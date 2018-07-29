from __future__ import absolute_import
import unittest

from nac.core import BenchmarkLoader, BenchmarkRunner
from ._example import TimeArrayMultiplication


class TestBenchmarkRunner(unittest.TestCase):
    def test_run_suite(self):
        loader = BenchmarkLoader()
        suite = loader.load_cases(TimeArrayMultiplication)
        runner = BenchmarkRunner()
        runner.run_benchmark_suite(suite)
