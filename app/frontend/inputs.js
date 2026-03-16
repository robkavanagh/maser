(async () =>
{
	// Get HTML elements
	const figure = document.getElementById("figure");
	const button = document.getElementById("button");
	const results_info = document.getElementById("results_info");
	const results_error = document.getElementById("results_error");
	const box_template = document.getElementById("box_template");

	// Get initial values from backend
	const {values, labels} = await (await fetch('/send_initial_values')).json();

	// Function to send inputs for validation in backend
	async function send_current_params(values)
	{
		const validation = await fetch('/validate_inputs', {
			method: "POST", 
			headers: {"Content-Type": "application/json"}, 
			body: JSON.stringify(values)
		});

		// Valid inputs
		if (validation.ok){

			// Clear previous error messages
			clear_input_errors();
			results_error.textContent = "";

			// Show computing cue
			results_info.textContent = "Computing...";
			figure.style.opacity = "0.3";
			button.style.opacity = "0.3";
			button.style.pointerEvents = "none";

			// Compute time series
			const result = await fetch('/run_maser', {
				method: "POST",
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify(values)
			});
			
			const data = await result.json();

			// Update figure
			figure.src = "data:image/png;base64," + data.fig;

			if (figure.style.visibility === "hidden"){
				figure.style.visibility = "visible";
			}
			
			// Update button
			button.href = "data:text/csv;base64," + data.csv;
			button.download = "MASER time series.csv";

			if (button.style.visibility === "hidden"){
				button.style.visibility = "visible";
			}

			// Clear loading indicator
			results_info.textContent = "";
			figure.style.opacity = "1";
			button.style.opacity = "1";
			button.style.pointerEvents = "";
		}

		// Invalid input(s)
		else {

			clear_input_errors();

			results_info.textContent = "";
			results_error.textContent = "- Invalid input";
			figure.style.visibility = "hidden";
			button.style.visibility = "hidden";

			const response = await validation.json();

			for (const error of response.detail){

				const key = error.loc[error.loc.length - 1];

				if (error.type === "float_parsing"){
					document.getElementById(key + "_error").textContent = "- Enter a valid number";
				}

				else if (error.type === "value_error"){
					document.getElementById(key + "_error").textContent = error.msg.replace("Value error, ", "");
				}

				else {
					document.getElementById(key + "_error").textContent = error.msg;
				}
			}
		}
	}

	// Initialise current values
	let current_values = values;
	let input_error_ids = {};

	// Function to clear input errors
	function clear_input_errors()
	{
		for (const id of Object.values(input_error_ids)){
			document.getElementById(id).textContent = "";
		}
	}

	// Draw box for each parameter
	for (const [group, params] of Object.entries(values))
	{
		const container = document.getElementById(group);

		for (const [key, value] of Object.entries(params))
		{
			const box = box_template.content.cloneNode(true);

			box.querySelector(".box_label").textContent = labels[group][key];
			box.querySelector(".box_input").id = key;
			box.querySelector(".box_input").value = value;
			box.querySelector(".box_error").id = key + "_error";

			input_error_ids[key] = key + "_error";

			// Set input type for date and time parameters
			if (key === "epoch"){
				box.querySelector(".box_input").type = "date";
			}

			else if (key === "t_start"){
				box.querySelector(".box_input").type = "time";
			}

			container.appendChild(box);

			// Validate changes to inputs
			document.getElementById(key).addEventListener("change", async () => {
				current_values[group][key] = document.getElementById(key).value;
				await send_current_params(current_values);
			});
		}
	}

	// Compute results for initial values
	await send_current_params(current_values);

})();