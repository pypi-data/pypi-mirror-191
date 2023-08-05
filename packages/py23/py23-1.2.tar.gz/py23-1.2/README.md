# Library py23
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/py23/pep257.yml?label=Pep257&style=plastic&branch=main)](https://github.com/vb64/py23/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/py23/py2.yml?label=Python%202.7&style=plastic&branch=main)](https://github.com/vb64/py23/actions?query=workflow%3Apy2)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/py23/py3.yml?label=Python%203.7-3.10&style=plastic&branch=main)](https://github.com/vb64/py23/actions?query=workflow%3Apy3)

Python 2/3 compatible functions

## Installation

```bash
$ pip install py23
```

## Usage

```python
import os
from py23 import load_module_by_path

py_module = load_module_by_path(os.path.join('py23', '__init__.py')
assert callable(py_module.remove_symbols)
```

## Development

```
$ git clone git@github.com:vb64/py23.git
$ cd py23
```
With Python 3:
```
$ make setup PYTHON_BIN=/path/to/python3
$ make tests
```
With Python 2:
```
$ make setup2 PYTHON_BIN=/path/to/python2
$ make tests2
```
