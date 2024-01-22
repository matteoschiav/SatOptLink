# SatOptLink
This repository contains some tools for the calculation of satellite trajectory, atmospheric attenuation and channel transmittance.

## Dependencies

SatOptLink depends on various other libraries:

* Standard scientific computing libraries, like [`numpy`](https://numpy.org/) and [`matplotlib`](https://matplotlib.org/)
* [`orekit`](https://gitlab.orekit.org/orekit-labs/python-wrapper/-/wikis/home) to compute the actiual orbits.

Note that we are actually using apython wrapper around `orekit` and its installation is not totally trivial. 