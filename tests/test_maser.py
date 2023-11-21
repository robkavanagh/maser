import numpy as np
import jax.numpy as jnp

from maser import maser 


# Defining variables 
# Stuff for MASER

# Stellar parameters
M_s = 0.5 # Star mass (solar masses) 
R_s = 0.75 # Star radius (solar radii) 
P_s = 4.86 # Star rotation period (days) 
i_s = 90 # Star inclination of the rotation axis relative to the line of sight (degrees) 
B_s = 430 # Star dipole field strength at the magnetic poles (Gauss) 
beta = 20 # Star magnetic obliquity (degrees)
phi_s0 = 0.2 # Star rotation phase at times = 0 (0 – 1)

# Planet parameters
a = 10 # Planet orbital distance (stellar radii) #### REFERENCE 
i_p = 89.18 # Planet inclination of the orbital axis relative to the line of sight (degrees)
lam = 0 # Planet projected spin-orbit angle (degrees) 
phi_p0 = 0.6 # Planet orbital phase at times = 0 (0 – 1) 

# Emission parameters
f = 10 # Emission observing frequency (MHz) 
alpha = 75 # Emission cone opening angle (degrees) 
dalpha = 5 # Emission cone thickness (degrees)

# Extra stuff 
P_p = 8.4630351 # AU Mic b period (days)


def test_maser():
    visibility_North, visibility_South = maser(M_s, R_s, P_s, i_s, B_s, beta, phi_s0, a, i_p, lam, phi_p0, f, alpha, dalpha, times)

    # check all finite
    assert np.all(np.isfinite(visibility_North))
    assert np.all(np.isfinite(visibility_South))
    
    #checksums on both sides
    assert visibility_South.sum() == 1297.
    assert np.isclose(visibility_North.std(),0.17732385) 
    assert visibility_North.sum() == 1300.
    assert np.isclose(visibility_South.std(),0.17712599)
