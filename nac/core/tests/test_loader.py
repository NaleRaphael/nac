from __future__ import absolute_import
import unittest

from nac.core import BenchmarkLoader
from . import _example
from ._example import TimeArrayMultiplication


class TestBenchmarkLoader(unittest.TestCase):
    def test_load_cases(self):
        tests = TimeArrayMultiplication.func_list
        loader = BenchmarkLoader()
        suite = loader.load_cases(TimeArrayMultiplication)
        for case in suite:
            self.assertTrue(case.func_name in tests)

    def test_load_cases_from_module(self):
        loader = BenchmarkLoader()
        suite = loader.load_cases_from_module(_example)
        self.assertTrue(len(suite) > 0)

    def test_discover(self):
        import os
        cur_dir = os.path.dirname(__file__)
        cur_dir_name = os.path.basename(cur_dir)
        loader = BenchmarkLoader()
        suite = loader.discover(start_dir=cur_dir, 
                                pattern_dir=cur_dir_name,
                                pattern_file='_example.py')
        self.assertTrue(len(suite) > 0)
