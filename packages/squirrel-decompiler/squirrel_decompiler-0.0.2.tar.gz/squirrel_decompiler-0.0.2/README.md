NutCracker - Squirrel-Lang bytecode cracker, used to decompile .cnut bytecode
==============

![github-stars][stars-badge]

|      CI              | status |
|----------------------|--------|
| Linux/macOS Travis   | [![Travis-CI][travis-badge]][travis-link] |
| MSVC 2019            | [![AppVeyor][appveyor-badge]][appveyor-link] |
| pip builds           | [![Pip Actions Status][actions-pip-badge]][actions-pip-link] |
| [`cibuildwheel`][]   | [![Wheels Actions Status][actions-wheels-badge]][actions-wheels-link] |

[stars-badge]:             https://img.shields.io/github/stars/shabbywu/NutCracker?style=social
[actions-pip-link]:        https://github.com/shabbywu/NutCracker/actions/workflows/pip.yml
[actions-pip-badge]:       https://github.com/shabbywu/NutCracker/workflows/Pip/badge.svg
[actions-wheels-link]:     https://github.com/shabbywu/NutCracker/actions/workflows/wheels.yml
[actions-wheels-badge]:    https://github.com/shabbywu/NutCracker/workflows/Wheels/badge.svg
[travis-link]:             https://travis-ci.org/shabbywu/NutCracker
[travis-badge]:            https://travis-ci.org/shabbywu/NutCracker.svg?branch=master&status=passed
[appveyor-link]:           https://ci.appveyor.com/project/shabbywu/NutCracker
[appveyor-badge]:          https://ci.appveyor.com/api/projects/status/f04io15t7o63916y

An project built with [pybind11](https://github.com/pybind/pybind11).
This requires Python 3.7+; for older versions of Python, check the commit
history.

Installation
------------

 - clone this repository
 - `pip install ./nutcracker`


License
-------

pybind11 is provided under a BSD-style license that can be found in the LICENSE
file. By using, distributing, or contributing to this project, you agree to the
terms and conditions of this license.

Test call
---------

```python
import nutcracker
with open("*.cnut", mode="rb") as fh:
    nut = nutcracker.decompile(fh.read())
```

[`cibuildwheel`]:          https://cibuildwheel.readthedocs.io
