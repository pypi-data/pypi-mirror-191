# halospec
[![PyPI version](https://badge.fury.io/py/halospec.svg)](https://badge.fury.io/py/halospec)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![automated tests](https://github.com/benjaminpope/halospec/actions/workflows/tests.yml/badge.svg)](https://github.com/benjaminpope/halospec/actions/workflows/tests.yml)

Halo Spectroscopy for JWST

Contributors: [Benjamin Pope](https://github.com/benjaminpope)

## What is halospec?

halospec - currently a placeholder - is a repository and package for halo spectroscopy of saturated sources in JWST/MIRI, using [jax](https://github.com/google/jax) to implement Total Variation minimization (TV-min) by gradient descent. This is an evolution of the idea of halo photometry as implemented in [halophot](https://github.com/hvidy/halophot) for K2.

## Installation

halospec is hosted on PyPI (though this is currently a placeholder): the easiest way to install this is with 

```
pip install halospec
```

You can also build from source. To do so, clone the git repo, enter the directory, and run

```
pip install .
```

We encourage the creation of a virtual enironment to run halospec to prevent software conflicts as we keep the software up to date with the lastest version of the core packages.


## Use & Documentation

Documentation will be found [here](https://benjaminpope.github.io/halospec/), though this is currently a placeholder. 

## Collaboration & Development

We are always looking to collaborate and further develop this software! We have focused on flexibility and ease of development, so if you have a project you want to use halospec for, but it currently does not have the required capabilities, don't hesitate to [email me](b.pope@uq.edu.au) and we can discuss how to implement and merge it! Similarly you can take a look at the `CONTRIBUTING.md` file.