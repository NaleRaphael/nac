from __future__ import absolute_import

import os
import sys
from fnmatch import fnmatch
from . import case
from . import suite

__all__ = ['BenchmarkLoader']

class BenchmarkLoader(object):
    bench_prefix = 'time'
    suite_class = suite.BenchmarkSuite
    case_class = case.BenchmarkCase

    def _find_benchmark_case_files(self, start_dir, pattern_dir, pattern_file):
        entry = os.path.abspath(start_dir)
        result = []
        for root, dirs, files in os.walk(entry):
            if len(files) == 0:
                continue
            if not fnmatch(os.path.basename(root), pattern_dir):
                continue
            result.extend([os.path.join(root, f) for f in files if fnmatch(f, pattern_file)])
        return result

    def discover(self, start_dir='.', pattern_dir='benchmarks', 
                 pattern_file='bench_*.py'):
        case_files = self._find_benchmark_case_files(start_dir, pattern_dir, pattern_file)
        suite = self.suite_class()
        for f in case_files:
            name = os.path.basename(f).split('.')[0]
            des = ('.py', 'U', 1)   # (suffix, mode, type: PY_SOURCE)
            mod = _load_module(name, f, info=des)
            su = self.load_cases_from_module(mod)
            suite.add_suite(su)
        return suite

    def load_cases(self, case_class):
        if not issubclass(case_class, self.case_class):
            raise TypeError('Given case is not a subclass of `{}`.'.format(self.case_class))
        names = self.get_case_names(case_class)
        suite = self.suite_class(map(case_class, names))
        return suite

    def get_case_names(self, case_class):
        def is_bench_func(attrname, case_class=case_class, 
                            prefix=self.bench_prefix):
            return (attrname.startswith(prefix) and 
                hasattr(getattr(case_class, attrname), '__call__'))
        names = [v for v in dir(case_class) if is_bench_func(v)]
        return names

    def load_cases_from_module(self, mod):
        suite = self.suite_class()
        for v in dir(mod):
            attr = getattr(mod, v)
            if not isinstance(attr, type) or not issubclass(attr, self.case_class):
                continue
            # In case that user imports case_class by `from XXX import case_class`
            if attr is self.case_class:
                continue
            su = self.load_cases(attr)
            suite.add_cases([case for case in su])
        return suite
