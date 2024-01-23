# SatOptLink
This repository contains some tools for the calculation of satellite trajectory, atmospheric attenuation and channel transmittance.

## Dependencies

SatOptLink depends on various other libraries:

* Standard scientific computing libraries, like [`numpy`](https://numpy.org/) and [`matplotlib`](https://matplotlib.org/)
* [`orekit`](https://gitlab.orekit.org/orekit-labs/python-wrapper/-/wikis/home) to compute the actiual orbits.

Note that we are actually using apython wrapper around `orekit` and its installation is not totally trivial. 

## Development

### Git branches

Currently, the development is directly done on the `main` branch, until we have a usable tool.

The `orekitdata` branch contains extra orekit files which are sometimes useful. To update this branch, always use `git rebase main` (or equivalent)


### Credits

SatOptLink is developped by:

* Matteo Schiavon 
* Aeden Leal 
* Hanafi Issahane
* Frédéric Grosshans

