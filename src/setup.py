#!/bin/env python

from distutils.core import setup, Extension
import numpy 

setup (name = 'PySBIG',
       version = '0.04',
       description = 'This module can read SBIG image files.',
       author='Russell Valentine',
       author_email="russ@coldstonelabs.org",
       url="http://coldstonelabs.org",
       py_modules=["PySBIG", "cPySBIG"],
       ext_modules=[Extension("PySBIGuncompress", ["PySBIGuncompressmodule.c"])])
