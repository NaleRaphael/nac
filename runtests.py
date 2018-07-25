#!/usr/bin/env python
from __future__ import absolute_import, print_function
import unittest
import logging


def run_test():
    loader = unittest.TestLoader()
    tests = loader.discover('.')
    unittest.TextTestRunner().run(tests)


if __name__ == '__main__':
    run_test()
