# chebroots

Recursively finding **all** roots of continuous functions using Chebyshev polynomials.

## Demonstration

[![Binder](https://mybinder.org/badge_logo.svg)][launch-binder]

To use `chebroots`, first construct a `ChebRoots` object by providing it with the function whose roots should be found. Then, the `find_all_roots` method returns all roots in the specified interval as well as the numerical error at every root.
```python
from chebroots import ChebRoots
fun = lambda x: x**2 - 1
interval = [-2, +2]
roots, error = ChebRoots(fun).find_all_roots(interval)
```

The [Jupyter](https://jupyter.org) Notebooks (`.ipynb`) in the [docs](./docs/) directory provide more detailed examples, including how to set user-defined tolerances. They can be viewed directly, for example on GitHub, or opened and used interactively with [Binder](https://mybinder.org). To launch the latest version, click [here][launch-binder] or on the "launch binder" badge above.

## Development environment

First, `git clone` the repository to your local machine and navigate (`cd`) to the directory.

On a standard Python installation, use
```shell
pip install -e .
```
to install `chebroots` and its dependencies. Note the `.` to specify the current directory. The `-e/--editable` flag is optional but highly encouraged.

Alternatively, if you are using the [conda](https://conda.io) package manager, you can use
```shell
conda env create -f environment.yml
```
to install `chebroots`, its dependencies, and additional (development) tools automatically. By default this creates an environment with name `chebroots-dev`, but that can be changed with the optional `-n YOUR-NAME` argument. The development environment is specified in [environment.yml](./environment.yml), which was created with
```shell
conda env export --name chebroots-dev --from-history | grep --invert-match '^prefix:' > environment.yml
```

## Code formatting

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![black](https://github.com/janniklasrose/chebroots/actions/workflows/black.yml/badge.svg?branch=main)](https://github.com/janniklasrose/chebroots/actions/workflows/black.yml)

`chebroots` uses [black](https://github.com/psf/black) for code formatting. A [GitHub Action](./.github/workflows/black.yml) automatically checks that all Python code is properly formatted. Before committing any changes to the code, run the auto-formatter:
```shell
black src/ 
```

[launch-binder]: https://mybinder.org/v2/gh/janniklasrose/chebroots/HEAD
