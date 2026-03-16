import numpy as np
from numba import njit
from maser import maser
from time import process_time

rad_per_deg = np.pi / 180

maser_numba = njit(cache = True)(maser)

nsamples = 100

times = np.linspace(0, 1, 1000)

times_base = np.array([])
times_numba = np.array([])

for i in range(nsamples):

	# Randomly sample the stellar parameters
	M_s = np.random.uniform(0.1, 1)
	R_s = np.random.uniform(0.1, 1)
	P_s = np.random.uniform(1, 100)
	i_s = np.random.uniform(0, 90) * rad_per_deg
	B_s = np.random.uniform(100, 1000)
	beta = np.random.uniform(0, 90) * rad_per_deg
	phi_s0 = np.random.uniform(0, 1)

	# Randomly sample the planetary parameters
	a = np.random.uniform(1, 100)
	i_p = np.random.uniform(0, 90) * rad_per_deg
	lam = np.random.uniform(0, 360) * rad_per_deg
	phi_p0 = np.random.uniform(0, 1)

	# Randomly sample the emission cone parameters
	f = np.random.uniform(10, 1000)
	alpha = np.random.uniform(60, 90) * rad_per_deg
	dalpha = np.random.uniform(1, 10) * rad_per_deg

	params = M_s, R_s, P_s, i_s, B_s, beta, phi_s0, a, i_p, lam, phi_p0, f, alpha, dalpha

	# Time base maser calculation
	t0 = process_time()
	maser(params, times)
	dt_base = process_time() - t0
	
	t0 = process_time()
	maser_numba(params, times)
	dt_numba = process_time() - t0

	# Skip first call of maser_numba as it includes compilation time warmup
	if i > 0:
		times_base = np.append(times_base, dt_base)
		times_numba = np.append(times_numba, dt_numba)

speedup = times_base / times_numba
print('Numba version is %d±%d times faster'%(np.average(speedup), np.std(speedup)))
