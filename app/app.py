import numpy as np
from numba import njit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import drange, DateFormatter, AutoDateLocator
from datetime import datetime, timedelta, timezone, date, time
from maser import maser, constants as c
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
import io
import csv
import base64


######################################################
# Setup
######################################################

# Set figure rendering and styling
matplotlib.use('Agg')
plt.style.use('frontend/style.mplstyle')
matplotlib.font_manager.fontManager.addfont('frontend/assets/Montserrat-Medium.ttf')
plt.rcParams['font.family'] = 'Montserrat'

# Constants
rad_per_deg = np.pi / 180
t_1970 = 2440587.5			# JD of 1970-01-01 00:00 UTC
npts_max = int(1e5)			# Max number of data points allowed

# Time series header string
time_series_header = Path('csv_header.txt').read_text()

# MASER function compiled with Numba
maser_numba = njit(cache = True)(maser)


######################################################
# Default parameters and valid ranges
######################################################

class star(BaseModel):
	M_s: float = Field(0.2, description = "Mass (solar masses):", gt = 0)
	R_s: float = Field(0.3, description = "Radius (solar radii):", gt = 0)
	P_s: float = Field(0.8, description = "Rotation period (days):", gt = 0)
	i_s: float = Field(67, description = "Inclination (degrees):", ge = 0, le = 90)
	B_s: float = Field(1000, description = "Magnetic field strength (Gauss):", gt = 0)
	beta: float = Field(34, description = "Magnetic obliquity (degrees):", ge = 0, le = 90)
	phi_s0: float = Field(0.1, description = "Rotation phase at reference time (0-1):", ge = 0, le = 1)

class planet(BaseModel):
	a: float = Field(5, description = "Orbital distance (stellar radii):", gt = 1)
	i_p: float = Field(56, description = "Orbital inclination (degrees):", ge = 0, le = 90)
	lam: float = Field(23, description = "Projected spin-orbit angle (degrees):", ge = 0, lt = 360)
	phi_p0: float = Field(0.6, description = "Orbital phase at reference time (0-1):", ge = 0, le = 1)

class cone(BaseModel):
	alpha: float = Field(75, description = "Opening angle (degrees):", ge = 0, le = 90)
	dalpha: float = Field(5, description = "Thickness (degrees):", gt = 0, le = 90)

class obs(BaseModel):
	epoch: str = Field("2026-01-01", description = "Epoch (DD/MM/YYYY):")
	t_start: str = Field("00:00", description = "Start time (UTC):")
	duration: float = Field(12, description = "Duration (hours):", gt = 0)
	dt: float = Field(10, description = "Temporal resolution (s):", gt = 0)
	f: float = Field(100, description = "Frequency (MHz):", gt = 0)
	t_ref: float = Field(2461041.5, description = "Reference time for phases (Julian date):", gt = 0)

	# Epoch formatting
	@field_validator('epoch')
	@classmethod
	def validate_epoch(cls, value):
		
		try: date.fromisoformat(value)
		except ValueError: raise ValueError('- Enter a valid date')
		return value

	# Time formatting
	@field_validator('t_start')
	@classmethod
	def validate_t_start(cls, value):

		try: time.fromisoformat(value)
		except ValueError: raise ValueError('- Enter a valid time')
		return value

class params(BaseModel):
	star_params: star = star()
	planet_params: planet = planet()
	cone_params: cone = cone()
	obs_params: obs = obs()


######################################################
# App logic
######################################################

app = FastAPI()

# Send initial values to be drawn in frontend
@app.get('/send_initial_values')
def send_initial_values():

	values = {}
	labels = {}

	for group, field in params.model_fields.items():

		values[group] = {}
		labels[group] = {}
		
		for key, f in field.annotation.model_fields.items():

			values[group][key] = f.default
			labels[group][key] = f.description

	return JSONResponse(content = {"values": values, "labels": labels})

# Validate inputs
@app.post('/validate_inputs')
def validate_inputs(data: params): return {}

# Run MASER and plot the resulting time series 
@app.post('/run_maser')
def run_maser(data: params):

	star = data.star_params
	planet = data.planet_params
	cone = data.cone_params
	obs = data.obs_params

	# Angles in radians
	i_s_rad = star.i_s * rad_per_deg
	beta_rad = star.beta * rad_per_deg
	i_p_rad = planet.i_p * rad_per_deg
	lam_rad = planet.lam * rad_per_deg
	alpha_rad = cone.alpha * rad_per_deg
	dalpha_rad = cone.dalpha * rad_per_deg

	model_params = star.M_s, star.R_s, star.P_s, i_s_rad, star.B_s, beta_rad, star.phi_s0, planet.a, i_p_rad, lam_rad, planet.phi_p0, obs.f, alpha_rad, dalpha_rad

	# Times relative to 1970-01-01 00:00 (in days)
	t0 = datetime.strptime(obs.epoch + ' ' + obs.t_start, '%Y-%m-%d %H:%M')
	times = drange(t0, t0 + timedelta(hours = obs.duration), timedelta(seconds = obs.dt))

	# Prevents overloading the server resources
	if len(times) > npts_max:
		return JSONResponse(status_code = 400, content = {'detail': '- Over %d data points. Decrease duration or increase resolution.'%npts_max})

	# Compute lightcurve
	times_maser = times - obs.t_ref + t_1970 		# Time in MASER frame
	N, S = maser_numba(model_params, times_maser)
	N = N.astype(int)
	S = S.astype(int)

	# Make figure
	fig, (ax_N, ax_S) = plt.subplots(2, sharex = True, figsize = (6, 2))

	for ax in [ax_N, ax_S]:
		ax.set_ylim(0, 1)
		ax.set_yticks([])
		ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
		ax.xaxis.set_major_locator(AutoDateLocator(maxticks = 8))

	ax_N.set_ylabel('North')
	ax_S.set_ylabel('South')
	ax_S.set_xlabel('Time on %s (UTC)'%(obs.epoch))

	dt_days = obs.dt / c.sec_per_day
	edges = np.append(times - 0.5 * dt_days, times[-1] + 0.5 * dt_days)

	# Plot lightcurves
	ax_N.stairs(N, edges, ec = None, fc = 'xkcd:salmon', fill = True)
	ax_S.stairs(S, edges, ec = None, fc = 'xkcd:sky blue', fill = True)
	plt.subplots_adjust(left = 0.04, right = 0.98, bottom = 0.2, top = 0.95, hspace = 0.1)

	# Encode the figure
	fig_buffer = io.BytesIO()
	plt.savefig(fig_buffer, format = 'png', dpi = 300)
	plt.close(fig)
	fig_buffer.seek(0)
	fig_64 = base64.b64encode(fig_buffer.read()).decode('utf-8')

	# Lightcurve csv header
	csv_buffer = io.StringIO()
	current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
	csv_buffer.write(time_series_header % (current_time, *star.model_dump().values(), *planet.model_dump().values(), *cone.model_dump().values(), *obs.model_dump().values()))
	
	# Lightcurve data
	csv_buffer.write('Time (JD), N, S\n')
	csv.writer(csv_buffer).writerows(zip(times + t_1970, N, S))
	csv_buffer.seek(0)
	csv_64 = base64.b64encode(csv_buffer.getvalue().encode('utf-8')).decode('utf-8')

	# Send image and time series to frontend
	return JSONResponse(content = {'fig': fig_64, 'csv': csv_64})

# Get frontend files
app.mount('/', StaticFiles(directory = 'frontend', html = True))