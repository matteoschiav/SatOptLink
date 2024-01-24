# SatOptLink
This repository contains some tools for the calculation of satellite trajectory, atmospheric attenuation and channel transmittance.
It is currenly developped in [LIP6](www.lip6.fr)’s [QI team](https://qi.lip6.fr) for applications in space quantum networks.

It’s current state is full of hacks and hard-coded values, but we intend to have a set of useable tools soon.

## Dependencies

SatOptLink depends on various other libraries:

* Standard scientific computing libraries, like [`numpy`](https://numpy.org/) and [`matplotlib`](https://matplotlib.org/)
* [`orekit`](https://gitlab.orekit.org/orekit-labs/python-wrapper/-/wikis/home) to compute the actual orbits

Note that we are currently using a python wrapper around `orekit` and its installation is not totally trivial, to say the least.

## Development

### Git branches

Currently, the development is directly done on the `main` branch, until we have a usable tool.

The `orekitdata` branch contains extra orekit files which are sometimes useful. To update this branch, always use `git rebase main` (or equivalent)


### Credits

SatOptLink is developped by:

* Matteo Schiavon
* Aeden Leal
* Hanafi Issahnane
* Frédéric Grosshans
