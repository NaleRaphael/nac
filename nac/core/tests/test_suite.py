from __future__ import absolute_import
import unittest

from nac.core import BenchmarkSuite
from ._example import BenchArrayMultiplication


class TestBenchmarkSuite(unittest.TestCase):
    def test_create_suite(self):
        tests = BenchArrayMultiplication.func_list
        suite = BenchmarkSuite(map(BenchArrayMultiplication, tests))
        for case in suite:
            self.assertTrue(case.func_name in tests)
