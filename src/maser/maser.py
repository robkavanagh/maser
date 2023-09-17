# The MASER code for computing the visibility of polarised radio emission induced by a planet on its host star when in a sub-Alfvénic orbit.
# 
# See full details in Kavanagh & Vedantham (2023).
# 
# Version 1.0

import numpy as np

# Constants
Msun = 1.989e33
Rsun = 6.955e10
G = 6.674e-8
rad_per_deg = np.pi / 180
sec_per_day = 86400

# Max loop size (Rstar)
Lmax = 100

# Tolerance for solver
tol = 1e-2

# Zero vector
zero_vec = np.array([0.0, 0.0, 0.0])

# Inputs:
# - M_s:     Stellar mass (solar masses)
# - R_s:     Stellar radius (solar radii)
# - P_s:     Stellar rotation period (days)
# - i_s:     Stellar inclination (degrees)
# - B_s:     Dipole field strength at magnetic poles (Gauss)
# - beta:    Magnetic obliquity (degrees)
# - phi_s0:  Rotation phase at time zero (0 - 1)
# - a:       Orbital distance (stellar radii)
# - i_p:     Orbital inclination (degrees)
# - lam:     Projected spin-orbit angle (degrees)
# - phi_p0:  Orbital phase at time zero (0 - 1)
# - f:       Observing frequency (MHz)
# - alpha:   Cone opening angle (degrees)
# - dalpha:  Cone thickness (degrees)
# - times:   Times to compute the visibility at (days)
# 
# The function returns two arrays of boolean values, which infer if emission is visible from the Northern (vis_N) and Southern (vis_S) magnetic hemispheres at each element of the times array.

def maser(M_s, R_s, P_s, i_s, B_s, beta, phi_s0, a, i_p, lam, phi_p0, f, alpha, dalpha, times):

	# Line of sight axes
	x = np.array([1, 0, 0])
	y = np.array([0, 1, 0])
	z = np.array([0, 0, 1])

	# Visibility arrays
	ntimes = len(times)
	vis = np.full((2, ntimes), False)

	# Skip sample if emission at frequency f is not possible
	if f > 2.8 * B_s: return vis

	# Planet orbital period (days)
	P_p = 2 * np.pi * ((a * R_s * Rsun) ** 3 / (G * M_s * Msun)) ** 0.5 / sec_per_day

	# Angles to rad
	i_s *= rad_per_deg
	beta *= rad_per_deg
	i_p *= rad_per_deg
	lam *= rad_per_deg
	alpha *= rad_per_deg
	dalpha *= rad_per_deg

	# Trig terms
	sin_i_s = np.sin(i_s)
	cos_i_s = np.cos(i_s)
	sin_lam = np.sin(lam)
	cos_lam = np.cos(lam)

	# Stellar coordinates
	z_s = cos_i_s * x + sin_i_s * z
	n_s = sin_i_s * x - cos_i_s * z

	# Plane of sky vectors for planet
	y1 = cos_lam * y - sin_lam * z
	z1 = sin_lam * y + cos_lam * z


	##################################################
	# Time loop
	##################################################

	for j, t in enumerate(times):

		##################################################
		# Compute vectors
		##################################################

		# Rotation phase (rad)
		phi_s = 2 * np.pi * (phi_s0 + t / P_s)

		# Planet orbital phase (rad)
		phi_p = 2 * np.pi * (phi_p0	+ t / P_p)

		# Stellar coordinates
		x_s = np.cos(phi_s) * n_s + np.sin(phi_s) * y

		# Magnetic pole
		z_B = np.sin(beta) * x_s + np.cos(beta) * z_s

		# Planet coordinates
		n_p = np.sin(i_p) * x - np.cos(i_p) * z1
		x_p = np.sin(phi_p) * y1 + np.cos(phi_p) * n_p

		# Magnetic latitude of planet
		cos_theta_p = np.sum(x_p * z_B)
		sin_theta_p = (1 - cos_theta_p ** 2) ** 0.5

		# Loop size
		if sin_theta_p == 0: L = np.inf
		else: L = a / sin_theta_p ** 2

		# Min and max frequency on field line
		f_min = 1.4 * B_s * L ** -3
		f_max = 2.8 * B_s * (1 - 0.75 / L) ** 0.5

		# Planet frequency (MHz)
		f_p = 2.8 * B_s * (a ** -3) * (1 - 0.75 * a / L) ** 0.5

		# Skip time if emission cannot occur at frequency f on the field line
		if ((f > f_max) | (f < f_min)) | ((L > Lmax) & (f_p > f)): continue

		# Magnetic equator
		if L == np.inf: x_B = zero_vec
		else: x_B = x_p / sin_theta_p - (cos_theta_p / sin_theta_p) * z_B


		##################################################
		# Solve for radius of emitting point
		##################################################

		# Field strength of emitting point
		B_f = f / 2.8

		# Initialise solver
		r_i = 1
		B_i = B_s * (1 - 0.75 / L) ** 0.5

		# Loop until frequency difference is less than tolerance set
		while np.abs(1 - B_i / B_f) > tol:

			F_i = (B_f / B_s) ** 2 * r_i ** 6 + 0.75 * r_i / L - 1
			dF_i = 6 * (B_f / B_s) ** 2 * r_i ** 5 + 0.75 / L
			r_i = r_i - F_i / dF_i
			B_i = B_s * r_i ** -3 * (1 - 0.75 * r_i / L) ** 0.5

		r_f = r_i


		##################################################
		# Visibility
		##################################################

		# Compute latitude of emission point in Northern hemisphere
		sin_theta_f = (r_f / L) ** 0.5
		cos_theta_f = (1 - sin_theta_f ** 2) ** 0.5

		# Cone components in Northern hemisphere in terms of x_B and z_B
		c_x = 3 * sin_theta_f * cos_theta_f / (1 + 3 * cos_theta_f ** 2) ** 0.5
		c_z = (3 * cos_theta_f ** 2 - 1) / (1 + 3 * cos_theta_f ** 2) ** 0.5

		# Check if emission generated in Northern hemisphere
		if ((cos_theta_p >= 0) & (f > f_p)) | ((cos_theta_p < 0) & (L < Lmax)):

			# Cone axis
			c_N = c_x * x_B + c_z * z_B

			# Angle between cone and line of sight (rad)
			gamma_N = np.arccos(c_N[0])

			# Visibility
			vis[0, j] = (alpha - dalpha / 2 < gamma_N) & (gamma_N < alpha + dalpha / 2)

		# Check if emission generated in Southern hemisphere
		if ((cos_theta_p < 0) & (f > f_p)) | ((cos_theta_p >= 0) & (L < Lmax)):

			# Cone axis
			c_S = c_x * x_B - c_z * z_B

			# Angle between cone and line of sight (rad)
			gamma_S = np.arccos(c_S[0])

			# Visibility
			vis[1, j] = (alpha - dalpha / 2 < gamma_S) & (gamma_S < alpha + dalpha / 2)

	return vis*1.0