# nd-core-lib

[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Core library for nDimensional.

## Table of Contents

- [Install](#install)
- [Usage](#usage)

## Install

To test the package in local, go into `nd-core-lib` (root folder) and run

```
pip install -e .
```

## Usage

To create the distribution,

```
python setup.py sdist
```

To upload the distribution to PyPI,

```
twine upload dist/* --verbose
```
