import numpy as np
import matplotlib.pyplot as plt
from maser import maser

rad_per_deg = np.pi / 180

########################################
# Define system parameters
########################################

# Stellar parameters
M_s = 0.2 					# Stellar mass (solar masses)
R_s = 0.3 					# Stellar radius (solar radii)
P_s = 0.8 					# Rotation period (days)
i_s = 67 * rad_per_deg		# Inclination (radians)
B_s = 1e3 					# Polar magnetic field strength (Gauss) 
beta = 34 * rad_per_deg 	# Magnetic obliquity (radians)
phi_s0 = 0.2 				# Stellar rotation phase at time zero (0-1)

# Planet parameters
a = 10						# Planet orbital distance (stellar radii)
i_p = 56 * rad_per_deg		# Planet orbital inclination (radians)
lam = 23 * rad_per_deg		# Projected spin-orbit angle (radians)
phi_p0 = 0.6				# Planet orbital phase at time zero (0-1)

# Emission parameters
f = 100						# Observing frequency (MHz)
alpha = 75 * rad_per_deg	# Emission cone opening angle (radians)
dalpha = 5 * rad_per_deg	# Emission cone thickness (radians)

# Observing times (days)
times = np.linspace(0, 2, 10000)


########################################
# Compute and plot lightcurve
########################################

params = M_s, R_s, P_s, i_s, B_s, beta, phi_s0, a, i_p, lam, phi_p0, f, alpha, dalpha
N, S = maser(params, times)

N = N.astype(int)
S = S.astype(int)

# Make figure
fig, (ax_N, ax_S) = plt.subplots(2, sharex = True, figsize = (6, 2))

for ax in [ax_N, ax_S]:
	ax.set_ylim(0, 1)
	ax.set_yticks([])

ax_N.set_ylabel('North')
ax_S.set_ylabel('South')
ax_S.set_xlabel('Time (days)')

dt = times[1] - times[0]
edges = np.append(times - 0.5 * dt, times[-1] + 0.5 * dt)

ax_N.stairs(N, edges, ec = None, fc = 'xkcd:salmon', fill = True)
ax_S.stairs(S, edges, ec = None, fc = 'xkcd:sky blue', fill = True)
plt.subplots_adjust(left = 0.04, right = 0.98, bottom = 0.25, top = 0.95, hspace = 0.1)

plt.show()
