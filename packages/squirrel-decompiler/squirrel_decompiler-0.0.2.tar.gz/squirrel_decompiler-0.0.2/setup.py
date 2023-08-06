import sys

# Available at setup time due to pyproject.toml
from pybind11 import get_cmake_dir
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.2"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/nutcracker/pull/53)

ext_modules = [
    Pybind11Extension("nutcracker",
        ["src/main.cpp", "src/stdafx.cpp", "src/BinaryReader.cpp", "src/Errors.cpp", "src/LFile.cpp", "src/LString.cpp", "src/NutDecompiler.cpp", "src/NutScript.cpp", "src/SqObject.cpp", "src/Statements.cpp"],
        # Example: passing in the version to the compiled code
        define_macros = [('VERSION_INFO', __version__)],
        ),
]

setup(
    name="squirrel_decompiler",
    version=__version__,
    author="shabbywu",
    author_email="shabbywu@qq.com",
    url="https://github.com/shabbywu/NutCracker",
    description="NutCracker - Squirrel-Lang bytecode cracker, used to decompile .cnut bytecode",
    long_description="""
NutCracker - Squirrel-Lang bytecode cracker, used to decompile .cnut bytecode
=============================================================================

.. figure:: https://img.shields.io/github/stars/shabbywu/NutCracker?style=social
   :alt: github-stars

   github-stars

+---------------------------------------------------+------------------+
| CI                                                | status           |
+===================================================+==================+
| Linux/macOS Travis                                | |Travis-CI|      |
+---------------------------------------------------+------------------+
| MSVC 2019                                         | |AppVeyor|       |
+---------------------------------------------------+------------------+
| pip builds                                        | |Pip Actions     |
|                                                   | Status|          |
+---------------------------------------------------+------------------+
| ```cibuil                                         | |Wheels Actions  |
| dwheel`` <https://cibuildwheel.readthedocs.io>`__ | Status|          |
+---------------------------------------------------+------------------+

An project built with `pybind11 <https://github.com/pybind/pybind11>`__.
This requires Python 3.7+; for older versions of Python, check the
commit history.

Installation
------------

-  clone this repository
-  ``pip install ./nutcracker``

License
-------

pybind11 is provided under a BSD-style license that can be found in the
LICENSE file. By using, distributing, or contributing to this project,
you agree to the terms and conditions of this license.

Test call
---------

.. code:: python

   import nutcracker
   with open("*.cnut", mode="rb") as fh:
       nut = nutcracker.decompile(fh.read())

.. |Travis-CI| image:: https://travis-ci.org/shabbywu/NutCracker.svg?branch=master&status=passed
   :target: https://travis-ci.org/shabbywu/NutCracker
.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/f04io15t7o63916y
   :target: https://ci.appveyor.com/project/shabbywu/NutCracker
.. |Pip Actions Status| image:: https://github.com/shabbywu/NutCracker/workflows/Pip/badge.svg
   :target: https://github.com/shabbywu/NutCracker/actions/workflows/pip.yml
.. |Wheels Actions Status| image:: https://github.com/shabbywu/NutCracker/workflows/Wheels/badge.svg
   :target: https://github.com/shabbywu/NutCracker/actions/workflows/wheels.yml

""",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
