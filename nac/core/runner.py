from __future__ import absolute_import

import os
import sys

from . import suite as nac_suite
from nac.logger import LogWriter

__all__ = ['BenchmarkRunner']

class BenchmarkRunner(object):
    logdir_name = 'bench_log'
    log_writer_class = LogWriter

    def __init__(self, log_writer_class=None):
        if log_writer_class is not None:
            if issubclass(log_writer_class, self.log_writer_class):
                self.log_writer_class = log_writer_class
            else:
                raise TypeError('`log_writer_class` should be a subclass of '
                                '{}'.format(self.log_writer_class))
        self._previous_class = None

    def _write_log(self, case, log):
        logdir = os.path.join(os.getcwd(), self.logdir_name)
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        logname = '{0}_{1}.{2}'.format(case.__class__.__name__, 
                                       case.func_name, 
                                       'csv')
        logpath = os.path.join(logdir, logname)
        writer = self.log_writer_class()
        writer.write(logpath, log)

    def _tear_down_previous_class(self, case):
        current_class = case.__class__
        if current_class == self._previous_class:
            return

        tear_down_class = getattr(current_class, 'tear_down_class', None)
        if tear_down_class is not None:
            try:
                tear_down_class()
            except:
                raise

    def _set_up_current_class(self, case):
        current_class = case.__class__
        if current_class == self._previous_class:
            return

        set_up_class = getattr(current_class, 'set_up_class', None)
        if set_up_class is not None:
            try:
                set_up_class()
            except:
                raise

    def run_benchmark(self, case):
        try:
            self._tear_down_previous_class(case)
            self._set_up_current_class(case)

            log = case.run()
            if case.enable_logging:
                self._write_log(case, log)

            # Update this only after case ran sucessfully
            self._previous_class = case.__class__
        except:
            raise

    def run_benchmark_suite(self, suite):
        if not isinstance(suite, nac_suite.BenchmarkSuite):
            raise TypeError('Given suite is not a instance of '
                            '{}.'.format(nac_suite.BenchmarkSuite))
        try:
            for case in suite:
                self.run_benchmark(case)

            self._tear_down_previous_class(None)
        except:
            raise
