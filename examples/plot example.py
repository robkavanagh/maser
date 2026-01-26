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

plt.plot(times, N, color = 'xkcd:light red', lw = 2, label = 'N')
plt.plot(times, S, color = 'xkcd:sky blue', lw = 2, label = 'S')
plt.legend(loc = 'lower right', title = 'Hemisphere')
plt.xlabel('Time (days)')
plt.ylabel('Signal visible?')
plt.yticks([0, 1], ['No', 'Yes'])
plt.tight_layout()
plt.show()
