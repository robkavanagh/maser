# MASER
`maser` (**M**agnetically inter**A**cting **S**tars and **E**xoplanets in the **R**adio) is a tool for computing the visibility of radio emission produced by magnetic star-planet interactions over time. It calculates the geometry of these interactions on the fly, based on the relevant system parameters. While it was developed for research on planet-hosting M-dwarfs, it is well suited for application to any magnetised body that can interact with an orbiting satellite (e.g. planets & brown dwarfs). It is written in [Python](https://www.python.org/), and is described in [Kavanagh & Vedantham (2023)](https://ui.adsabs.harvard.edu/abs/2023MNRAS.524.6267K).

# Installation
`maser` can be installed on Unix systems via `pip`:
```
pip install git+https://github.com/robkavanagh/maser.git
```

Its sole dependency is NumPy (>version 1.23).
# Basic usage
Once installed, you can import `maser` into a Python workflow via:
```
from maser import maser
```

The function `maser` requires the vector `params`, which contains the system parameters required to compute the visibility of the radio emission generated via the magnetic star-planet interactions, and the NumPy array `times`, which contains the observing times in days. Two optional parameters, `Lmax` and  `tol`, can also be set when calling `maser`, which set the maximum size of the magnetic field loops  and the tolerance of the numerical solver implemented (see [Kavanagh & Vedantham, 2023](https://ui.adsabs.harvard.edu/abs/2023MNRAS.524.6267K) for details).

The elements of `params` and their associated units are as follows:

**Star:**
- `M_s`: Mass (solar masses)
- `R_s`: Radius (solar radii)
- `P_s`: Rotation period (days)
- `i_s`: Inclination of the rotation axis relative to the line of sight (radians)
- `B_s`: Dipole field strength at the magnetic poles (Gauss)
- `beta`: Magnetic obliquity (radians)
- `phi_s0`: Rotation phase at ``times = 0`` (0 – 1)

**Planet:**
- `a`: Orbital distance (stellar radii)
- `i_p`: Inclination of the orbital axis relative to the line of sight (radians)
- `lam`: Projected spin-orbit angle (radians)
- `phi_p0`: Orbital phase at ``times = 0`` (0 – 1)

**Emission:**
- `f`: Observing frequency (MHz)
- `alpha`: Cone opening angle (radians)
- `dalpha`: Cone thickness (radians)

# Example calculation
The script `examples/plot example.py` contains example code of how to call `maser` for a single star-planet system observed over two days. Calling `maser(params, times)` returns two arrays, which correspond to the visibility of radio emission from the Northern and Southern magnetic hemispheres at each time element in `times`. Visible emission is represented with the value `True`, while emission that is either not visible or cannot be generated is represented with the value `False`. Plotting the computed lightcurves using e.g. [Matplotlib](https://matplotlib.org/) should resemble the following time series (where `vis_N` and `vis_S` are the visibilities of the emission from the Northern/Southern magnetic hemispheres):

<p align="center">
<img src="https://user-images.githubusercontent.com/24622499/232755000-d36b8aa1-d747-4c8a-a97c-0249238bb99e.png" width="80%"/>
</p>

# Acknowledging use of the code
If you use `maser` in your own work, please cite [Kavanagh & Vedantham (2023)](https://ui.adsabs.harvard.edu/abs/2023MNRAS.524.6267K).
