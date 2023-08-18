import numpy as np # for maths 
import matplotlib # for plotting 
import matplotlib as mpl
import matplotlib.pyplot as plt
#from emcee import MASER

import emcee.MASER as ms

# Setting directory

ddir = '/Users/katelynsmith/Desktop/Capstone/'


# Defining variables 

M_s = 0.5 # Star mass (solar masses) #### REFERENCE (PAPER 6 on one note) #####

R_s = 0.75 # Star radius (solar radii) ####  REFERENCE (PAPER 6 on one note) ####


P_s = 4.86 # Star rotation period (days) ####  REFERENCE (PAPER 6 on one note) ####


i_s = 90 # Star inclination of the rotation axis relative to the line of sight (degrees) ####  ACCORDING TO MEETING WITH BEN ####


B_s = 430 # Star dipole field strength at the magnetic poles (Gauss) #### https://arxiv.org/pdf/2304.09642.pdf #### 


beta = 20 # Star magnetic obliquity (degrees) #### ACCORDING TO MEETING WITH BEN ####


phi_s0 = 0.2 # Star rotation phase at times = 0 (0 – 1) <<<<<< LEFT AS IS


a = 18.5 # Planet orbital distance (stellar radii) #### REFERENCE (PAPER 6 on one note) ####
i_p = 89.18 # Planet inclination of the orbital axis relative to the line of sight (degrees) #### REFERENCE (PAPER 7 on one note) #### 
lam = 0 # Planet projected spin-orbit angle (degrees) #### ranging from -15 to 18 degrees REFERENCE Spin-orbit alignment and magnetic activity in the young planetary system AU Mic⋆ ####

P_p = 8.4630351 # AU Mic b period in days
phi_p0 = 0.6 # Planet orbital phase at times = 0 (0 – 1) <<<<< LEFT AS IS

f = 10 # Emission observing frequency (MHz) #### - MAY INCREASE TO 3 GHz REFERENCE (PAPER 6 on one note) ####


alpha = 75 # Emission cone opening angle (degrees) <<<<< LEFT THESE AS IS - BASED ON KAVANAGH 2023
dalpha = 5 # Emission cone thickness (degrees) <<<<< LEFT THESE AS IS - BASED ON KAVANAGH 2023

times = np.linspace(0, 40, 100000) # Array of observation times to compute (days)

# Call the function
vis_N, vis_S = ms.maser(M_s, R_s, P_s, i_s, B_s, beta, phi_s0, a, i_p, lam, phi_p0, f, alpha, dalpha, times)

# Plotting results
plt.plot(times, vis_N, color = '#A9561E')
plt.plot(times, vis_S, color = '#D1B26F')
#plt.plot(times % P_s, vis_N, color = '#A9561E')
# plt.plot(times % P_s, vis_S, color = '#D1B26F')
matplotlib.pyplot.text(-3.7, 1, 'On', fontdict=None, fontsize=11, color = '#DC143C')
matplotlib.pyplot.text(-3.7, 0, 'Off', fontdict=None, fontsize=11, color = '#DC143C')
matplotlib.pyplot.text(0.5, 0.95, 'North', fontdict=None, fontsize=11, color = '#A9561E')
matplotlib.pyplot.text(4.5, 0.95, 'South', fontdict=None, fontsize=11, color = '#D1B26F')
for j in range(8):
    plt.axvline(P_s * j+1,color='r',linestyle='--',alpha=0.5 )


plt.xlabel('Time (days)')
plt.ylabel('Signal visibility (unitless)')
plt.minorticks_on()
plt.grid()
plt.show()

