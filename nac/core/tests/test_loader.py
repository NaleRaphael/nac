from __future__ import absolute_import
import unittest

from nac.core import BenchmarkLoader
from ._example import BenchArrayMultiplication


class TestBenchmarkLoader(unittest.TestCase):
    def test_load_cases(self):
        tests = BenchArrayMultiplication.func_list
        loader = BenchmarkLoader()
        suite = loader.load_cases(BenchArrayMultiplication)
        for case in suite:
            self.assertTrue(case.func_name in tests)
