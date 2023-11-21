# MASER

[![integration](https://github.com/KSmithyy/maser/actions/workflows/tests.yml/badge.svg)](https://github.com/KSmithyy/maser/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](http://img.shields.io/badge/arXiv-2307.02555-blue.svg?style=flat)](http://arxiv.org/abs/2307.02555)
<!-- [![PyPI version](https://badge.fury.io/py/maser.svg)](https://badge.fury.io/py/maser) -->

The MASER (**M**agnetically inter**A**cting **S**tars and **E**xoplanets in the **R**adio) code is a flexible tool written in [Python](https://www.python.org/) (version `3.10.8`) for computing the visibility of polarised radio emission as a function of time from exoplanetary systems. The code computes the geometry relevant for magnetic star-planet interactions in the radio regime on the fly, based on a set of key physical and geometrical properties. While the code was developed with planet-hosting M dwarf systems in mind, it is also well-suited for application to any magnetised host-satellite system (i.e. planet-moon and brown dwarf-satellite systems). The code depends only on [NumPy](https://numpy.org/), and as such can be easily deployed on systems with Python installed. The current version of the code uses NumPy version `1.23.5`. A full description of the code can be found in [Kavanagh & Vedantham (2023)](https://arxiv.org/abs/2307.02555).

# Basic usage
MASER requires the following set of inputs in the order that they are listed, which describe the system properties and geometry. The units of each input are listed in brackets.

Star:
- `M_s`: Mass (solar masses)
- `R_s`: Radius (solar radii)
- `P_s`: Rotation period (days)
- `i_s`: Inclination of the rotation axis relative to the line of sight (degrees)
- `B_s`: Dipole field strength at the magnetic poles (Gauss)
- `beta`: Magnetic obliquity (degrees)
- `phi_s0`: Rotation phase at ``times = 0`` (0 – 1)

Planet:
- `a`: Orbital distance (stellar radii)
- `i_p`: Inclination of the orbital axis relative to the line of sight (degrees)
- `lam`: Projected spin-orbit angle (degrees)
- `phi_p0`: Orbital phase at ``times = 0`` (0 – 1)

Emission and time:
- `f`: Observing frequency (MHz)
- `alpha`: Cone opening angle (degrees)
- `dalpha`: Cone thickness (degrees)
- `times`: Array of times to compute (days)

# Example of the code in action
Calling the `maser()` function with the aforementioned inputs returns two arrays, which contain the visibility of emission from the Northern (`vis_N`) and Southern (`vis_S`) magnetic hemispheres at each time element in `times`. Visible emission is represented with the value `True`, while emission that is either not visible or cannot be generated is represented with the value `False`. See below for an example usage of the code to produce the \`visibility lightcurve' of radio emission from a system.
```python
# Define inputs
M_s = 0.2
R_s = 0.3
P_s = 0.8
i_s = 67
B_s = 1e3
beta = 34
phi_s0 = 0.2
a = 10
i_p = 56
lam = 23
phi_p0 = 0.6
f = 100
alpha = 75
dalpha = 5
times = np.linspace(0, 2, 10000)

# Call the function
vis_N, vis_S = maser(M_s, R_s, P_s, i_s, B_s, beta, phi_s0, a, i_p, lam, phi_p0, f, alpha, dalpha, times)
```
The visibility lightcurve computed should resemble the following:

![fig](https://user-images.githubusercontent.com/24622499/232755000-d36b8aa1-d747-4c8a-a97c-0249238bb99e.png)

# jit compilation with Jax
The code is automatically just-in-time compiled using Jax for accelerated computation.

# Acknowledging use of the code
We kindly ask that publications which make use of the MASER code cite [Kavanagh & Vedantham (2023)](https://arxiv.org/abs/2307.02555).
