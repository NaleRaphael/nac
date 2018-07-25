from __future__ import absolute_import

__all__ = ['BenchmarkSuite']

class BenchmarkSuite(object):
    def __init__(self, cases=()):
        self._cases = []
        self.add_cases(cases)

    def __iter__(self):
        return iter(self._cases)

    def add_case(self, case):
        if not hasattr(case, '__call__'):
            raise TypeError('Given case is not callable.')
        self._cases.append(case)

    def add_cases(self, cases):
        for case in cases:
            self.add_case(case)

    def add_suite(self, suite):
        if not isinstance(suite, BenchmarkSuite):
            raise TypeError('Given suite is not a isinstance of `BenchmarkSuite`.')
        for case in suite:
            self.add_case(case)
