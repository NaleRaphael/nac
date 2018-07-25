#!/usr/bin/env python
from __future__ import absolute_import, print_function
from setuptools import setup, find_packages

def setup_package():
    # semantic versioning
    MAJOR = 1
    MINOR = 0
    MICRO = 0
    VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

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
