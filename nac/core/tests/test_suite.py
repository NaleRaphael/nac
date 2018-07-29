from __future__ import absolute_import
import unittest

from nac.core import BenchmarkSuite
from ._example import TimeArrayMultiplication


class TestBenchmarkSuite(unittest.TestCase):
    def test_create_suite(self):
        tests = TimeArrayMultiplication.func_list
        suite = BenchmarkSuite(map(TimeArrayMultiplication, tests))
        for case in suite:
            self.assertTrue(case.func_name in tests)
