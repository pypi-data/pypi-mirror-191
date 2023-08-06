#!/usr/bin/env python

"""Setup script for the FROST2STAC package."""

from setuptools import setup, find_packages
import versioneer
from setuptools import setup

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)

