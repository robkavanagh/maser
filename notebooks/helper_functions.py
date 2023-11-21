# helper_functions.py

import numpy as np # for maths 
import matplotlib # for plotting 

from astropy.timeseries import LombScargle

from scipy.signal import find_peaks

from maser import maser

from tqdm import tqdm 

import warnings
warnings.filterwarnings("ignore")


'''------------------------------------------
---------------------------------------------'''

# Defining useful functions

# Constants
Msun = 1.989e33
Rsun = 6.955e10
G = 6.674e-8
rad_per_deg = np.pi / 180
sec_per_day = 86400


def get_P_p(a, M_s, R_s):
	return 2 * np.pi * ((a * R_s * Rsun) ** 3 / (G * M_s * Msun)) ** 0.5 / sec_per_day

def get_a(P_p, M_s, R_s):
    return ((P_p * sec_per_day / (2 * np.pi)) ** (2/3) * (G * M_s * Msun) ** (1/3) / (R_s * Rsun))

def get_events(t, vis):
    ups = np.where(np.diff(vis,1) > 0)[0]+1
    downs = np.where(np.diff(vis,1) < 0)[0]

    if ups[0] > downs[0]:
        downs = np.delete(downs,0)
    elif ups[-1] > downs [-1]:
        ups = np.delete(ups,-1)
    
    full_length = np.min([len(ups),len(downs)])
    ups, downs = ups[:full_length], downs[:full_length]

    durations = t[downs] - t[ups]
    centres = t[ups] + durations/2

    return centres, durations

def group_events(centres):
    durations = np.diff(centres)
    centres = centres[:-1] + durations/2

    return centres, durations

def get_oc(centres):
    mean_spacing = np.mean(np.diff(centres))
    predicted = centres[0] + (mean_spacing)*np.arange(len(centres))
    oc = centres-predicted
    return oc

def get_peaks(freqs, amps):
    peaks, metadata = find_peaks(amps,prominence=0.02)
    order = np.argsort(metadata['prominences'])[::-1]
    peaks, amps = freqs[peaks][order][:3], metadata['prominences'][order][:3]

    if len(peaks) < 3:
        peaks = np.concatenate([peaks,np.zeros(3-len(peaks))])
        amps = np.concatenate([amps,np.zeros(3-len(amps))])

    return peaks[:3], amps[:3]