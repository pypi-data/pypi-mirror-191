# pytask-environment

[![PyPI](https://img.shields.io/pypi/v/pytask-environment?color=blue)](https://pypi.org/project/pytask-environment)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytask-environment)](https://pypi.org/project/pytask-environment)
[![image](https://img.shields.io/conda/vn/conda-forge/pytask-environment.svg)](https://anaconda.org/conda-forge/pytask-environment)
[![image](https://img.shields.io/conda/pn/conda-forge/pytask-environment.svg)](https://anaconda.org/conda-forge/pytask-environment)
[![PyPI - License](https://img.shields.io/pypi/l/pytask-environment)](https://pypi.org/project/pytask-environment)
[![image](https://img.shields.io/github/actions/workflow/status/pytask-dev/pytask-environment/main.yml?branch=main)](https://github.com/pytask-dev/pytask-environment/actions?query=branch%3Amain)
[![image](https://codecov.io/gh/pytask-dev/pytask-environment/branch/main/graph/badge.svg)](https://codecov.io/gh/pytask-dev/pytask-environment)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pytask-dev/pytask-environment/main.svg)](https://results.pre-commit.ci/latest/github/pytask-dev/pytask-environment/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

______________________________________________________________________

pytask-environment allows you to detect changes in your pytask environment and abort a
project build.

## Installation

pytask-environment is available on [PyPI](https://pypi.org/project/pytask-environment)
and [Anaconda.org](https://anaconda.org/conda-forge/pytask-environment). Install it with

```console
$ pip install pytask-environment

# or

$ conda install -c conda-forge pytask-environment
```

## Usage

If the user attempts to build the project with `pytask build` and the Python version has
been cached in the database in a previous run, an invocation with a different
environment will produce the following command line output.

![image](_static/error.png)

Running

```console
$ pytask --update-environment
```

will update the information on the environment.

To disable either checking the path or the version, set the following configuration to a
falsy value.

```toml
[tool.pytask.ini_options]
check_python_version = false  # true by default

check_environment = false  # true by default
```

## Future development

The plugin might be further extended to compare the current environment against an
`environment.yml` or a list of packages and versions to ensure that the environment is
not altered.

## Changes

Consult the [release notes](CHANGES.md) to find out about what is new.
