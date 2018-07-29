from __future__ import absolute_import

import os
import re
import sys
from fnmatch import fnmatch
from . import case
from . import suite

__all__ = ['BenchmarkLoader']

case_type_dict = {
    'time': case.TimeBenchmarkCase,
    'mem': case.MemBenchmarkCase
}

class BenchmarkLoader(object):
    cls_basic_case = case.BenchmarkCase
    cls_basic_suite = suite.BenchmarkSuite
    re_pat = r'(?P<case_type>time|mem)_(\w+)'

    def __init__(self):
        self.regex = re.compile(self.re_pat)

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
        suite = self.cls_basic_suite()
        for f in case_files:
            name = os.path.basename(f).split('.')[0]
            des = ('.py', 'U', 1)   # (suffix, mode, type: PY_SOURCE)
            mod = _load_module(name, f, info=des)
            su = self.load_cases_from_module(mod)
            suite.add_suite(su)
        return suite

    def load_cases(self, case_class):
        if not issubclass(case_class, self.cls_basic_case):
            raise TypeError('Given case is not a subclass of `{}`.'.format(self.cls_basic_case))
        name_dict = self.classify_cases_by_name(case_class)
        suite = self.cls_basic_suite()
        for k in name_dict:
            names = name_dict[k]
            suite.add_suite(self.cls_basic_suite(map(case_class, names)))
        return suite

    def classify_cases_by_name(self, case_class):
        """ Make sure that cases of same type will be grouped. """
        name_dict = {k: [] for k in case_type_dict}
        for attrname in dir(case_class):
            match = self.regex.match(attrname)
            if match is not None and hasattr(getattr(case_class, attrname), '__call__'):
                case_type = match.group('case_type')
                name_dict[case_type].append(attrname)
        return name_dict

    def load_cases_from_module(self, mod):
        suite = self.cls_basic_suite()
        for v in dir(mod):
            attr = getattr(mod, v)
            if not isinstance(attr, type) or not issubclass(attr, self.cls_basic_case):
                continue
            # In case that user imports case_class by `from XXX import case_class`
            if attr is self.cls_basic_case:
                continue
            su = self.load_cases(attr)
            suite.add_cases([case for case in su])
        return suite


def _load_module(name, fn, info=None):
    import imp

    if info is None:
        path = os.path.dirname(fn)
        fo, fn, info = imp.find_module(name, [path])
    else:
        fo = open(fn, info[1])

    try:
        mod = imp.load_module(name, fo, fn, info)
    except:
        raise
    finally:
        fo.close()
    return mod
