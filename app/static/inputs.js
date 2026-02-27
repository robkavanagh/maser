// ######################################################
// Default parameters
// ######################################################

const initial_params = {
	star: [
		{key: "M_s", label: "Mass (solar masses):", default_val: 0.2},
		{key: "R_s", label: "Radius (solar radii):", default_val: 0.3},
		{key: "P_s", label: "Rotation period (days):", default_val: 0.8},
		{key: "i_s", label: "Inclination (degrees):", default_val: 67, min_val_allowed: true, max_val: 90, max_val_allowed: true},
		{key: "B_s", label: "Magnetic field strength (Gauss):", default_val: 1000},
		{key: "beta", label: "Magnetic obliquity (degrees):", default_val: 34, min_val_allowed: true, max_val: 90, max_val_allowed: true},
		{key: "phi_s0", label: "Rotation phase at reference time (0-1):", default_val: 0.1, min_val_allowed: true, max_val: 1, max_val_allowed: true}],

	planet: [
		{key: "a", label: "Orbital distance (stellar radii):", default_val: 5, min_val: 1},
		{key: "i_p", label: "Orbital inclination (degrees):", default_val: 56, min_val_allowed: true, max_val: 90, max_val_allowed: true},
		{key: "lam", label: "Projected spin-orbit angle (degrees):", default_val: 23, min_val_allowed: true, max_val: 360},
		{key: "phi_p0", label: "Orbital phase at reference time (0-1):", default_val: 0.6, min_val_allowed: true, max_val: 1, max_val_allowed: true}],

	cone: [
		{key: "alpha", label: "Opening angle (degrees):", default_val: 75, min_val_allowed: true, max_val: 90, max_val_allowed: true},
		{key: "dalpha", label: "Thickness (degrees):", default_val: 5, max_val: 90, max_val_allowed: true}],

	obs: [
		{key: "epoch", label: "Epoch (DD/MM/YYYY):", default_val: "2026-01-01"},
		{key: "t_start", label: "Start time (UTC):", default_val: "00:00"},
		{key: "duration", label: "Duration (hours):", default_val: 12},
		{key: "dt", label: "Temporal resolution (s):", default_val: 10},
		{key: "f", label: "Frequency (MHz):", default_val: 100},
		{key: "t_ref", label: "Reference time for phases (Julian date):", default_val: 2461041.5}]
}


// ######################################################
// Initialise current parameters
// ######################################################

const current_params = {};

for (const group in initial_params)
{
	current_params[group] = {};

	const params = initial_params[group];

	for (const param of params){
		current_params[group][param.key] = param.default_val;
	}
}


// ######################################################
// Manage updates to input parameters
// ######################################################

const url = "http://127.0.0.1:8000/run_maser";

const figure = document.getElementById("figure");
const button = document.getElementById("button");
const error = document.getElementById("error");

// Function to send inputs to backend
async function send_current_params()
{
	// Send current parameters to backend
	const response = await fetch(url, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(current_params)});

	// Get image and lightcurve csv
	const data = await response.json();

	// Clear previous error
	error.textContent = "";
	
	// Update figure
	figure.src = "data:image/png;base64," + data.fig;
	
	if (figure.style.visibility === "hidden") {
		figure.style.visibility = "visible";
	}

	// Update button
	button.href = "data:text/csv;base64," + data.csv;
	button.download = "MASER time series.csv";

	if (button.style.visibility === "hidden") {
		button.style.visibility = "visible";
	}
}

// Draw results for default parameters
send_current_params();


// ######################################################
// Error handling
// ######################################################

function invalid_input() {
	figure.style.visibility = "hidden";
	button.style.visibility = "hidden";
	error.textContent = "- Invalid input";
}


// ######################################################
// Input boxes
// ######################################################

function create_input_boxes(container, group, param)
{
	// Get HTML template for input box
	const box = document.getElementById("box_template").content.cloneNode(true);
	const box_label = box.querySelector(".box_label");
	const box_input = box.querySelector(".box_input");
	const box_error = box.querySelector(".box_error");

	box_label.textContent = param.label;
	box_input.value = param.default_val;

	let box_type = "number";

	if (param.key === "epoch"){
		box_type = "date";
		box.querySelector(".box_input").type = box_type;
	}

	else if (param.key === "t_start"){
		box_type = "time";
		box.querySelector(".box_input").type = box_type;
	}

	// Initialise min/max vals - fallback to defaults if not specified
	const min_val = param.min_val ?? 0;
	const max_val = param.max_val ?? Infinity;
	const min_val_allowed = param.min_val_allowed ?? false;
	const max_val_allowed = param.max_val_allowed ?? false;

	// This triggers with every change to a box
	function box_update()
	{
		// Clear prev error
		box_error.textContent = "";

		let current_value = box_input.value;

		// Empty input/invalid date or time
		if (current_value === ""){
			if (box_type == "date"){
				box_error.textContent = "- Enter a valid date";
			}

			else if (box_type == "time"){
				box_error.textContent = "- Enter a valid time";
			}

			else{
				box_error.textContent = "- Value required";
			}

			invalid_input();
			return;
		}

		// Numeric inputs
		if (box_type == "number"){
			if (current_value === ""){
				box_error.textContent = "- Value required";
				invalid_input();
				return;
			}
			
			else if (isNaN(current_value)){
				box_error.textContent = "- Enter a valid number";
				invalid_input();
				return;
			}

			else if (current_value <= min_val && !min_val_allowed){
				box_error.textContent = `- Enter a value > ${min_val}`;
				invalid_input();
				return;
			}

			else if (current_value < min_val && min_val_allowed){
				box_error.textContent = `- Enter a value ≥ ${min_val}`;
				invalid_input();
				return;
			}

			else if (current_value >= max_val && !max_val_allowed){
				box_error.textContent = `- Enter a value < ${max_val}`;
				invalid_input();
				return;
			}

			else if (current_value > max_val && max_val_allowed){
				box_error.textContent = `- Enter a value ≤ ${max_val}`;
				invalid_input();
				return;
			}
		}

		// Only if input is valid
		current_params[group][param.key] = current_value;
		send_current_params();
	}

	// Create a listener to monitor current values
	box_input.addEventListener("change", box_update);

	container.appendChild(box);
}


// ######################################################
// Initialise input boxes
// ######################################################

// Sections of input region
const containers = ["stellar_params", "planet_params", "cone_params", "obs_params"];

for (i in containers)
{
	const container = document.getElementById(containers[i]);
	const group = Object.keys(initial_params)[i];

	for (param of initial_params[group]){
		create_input_boxes(container, group, param);
	}
}