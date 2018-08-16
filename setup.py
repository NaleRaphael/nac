#!/usr/bin/env python
from __future__ import absolute_import, print_function
from setuptools import setup, find_packages

import sys

if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins

builtins.__NAC_SETUP__ = True

# semantic versioning
MAJOR = 0
MINOR = 1
MICRO = 0
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


def write_version_py(version_string, fn='nac/version.py'):
    content = """
# This file is generated from setup.py
version = '{version}'
"""

    f = open(fn, 'w')
    try:
        f.write(content.format(version=version_string))
    finally:
        f.close


def setup_package():
    write_version_py(VERSION)

    # package to be installed
    EXCLUDED = []
    PACKAGES = find_packages(exclude=EXCLUDED)

    REQUIREMENTS = [
        'numpy>=1.9.1',
        'matplotlib>=1.4.2',
    ]

    metadata = dict(
        name='nac',
        version=VERSION,
        description='Write your microbenchmark scripts in unittest-like way.',
        url='https://github.com/NaleRaphael/nac',
        packages=PACKAGES,
        install_requires=REQUIREMENTS
    )

    setup(**metadata)


if __name__ == '__main__':
    try:
        setup_package()
    except Exception as ex:
        print(ex.message)
