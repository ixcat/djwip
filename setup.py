#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import sys

here = path.abspath(path.dirname(__file__))

long_description = """"
DJWip - work-in-progress and other misc DataJoint utilities.
see README.md for further information.
"""

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split()

setup(
    name='djwip',
    version='0.0.1',
    description="DataJoint WIP",
    long_description=long_description,
    author='TODO: Correct Attribution',
    author_email='TODO: Correct Maintainer Email',
    license='TODO: Resolve',
    url='https://github.com/datajoint/djwip',
    keywords='datajoint',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requirements,
)
