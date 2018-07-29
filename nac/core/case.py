from __future__ import absolute_import, division

import sys
import time
import numpy as np

# Definition in `timeit` module
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

__all__ = ['BenchmarkCase', 'TimeBenchmarkCase', 'MemBenchmarkCase']

class BenchmarkCase(object):
    data = None

    def __init__(self, func_name, enable_logging=True, stream=sys.stderr):
        self.func_name = func_name
        self.enable_logging = enable_logging
        self.stream = stream

        # Default arguments for benchmark. User can modify them in `self.set_up()`
        self.args = ()
        self.kwargs = {}
        self.step = 100
        self.rd = 3

    def set_up(self):
        pass

    def tear_down(self):
        pass

    @classmethod
    def set_up_class(cls):
        pass

    @classmethod
    def tear_down_class(cls):
        pass

    def _check_bench_args(self):
        if self.data is None:
            raise ValueError('No data availabe.')
        if self.step < 1:
            raise ValueError('Step should not be less than 1.')
        if len(self.data) // self.step < 1:
            raise ValueError('Size of data is not large enough to be partitioned'
                'proportionally. It should at least equal to `step`.')

    def run(self):
        raise NotImplementedError('This method should be implemented in subclass.')

    def __call__(self):
        return self.run()


class TimeBenchmarkCase(BenchmarkCase):
    def run(self):
        try:
            self.set_up()
            self._check_bench_args()
        except:
            raise
        self.stream.write('Current running: {}\n'.format(self.func_name))

        # NOTE:
        # 1. First row should be zero (no data input) -> self.step + 1
        # 2. Data length in each step should be written in log too -> self.rd + 1
        tlog = np.zeros((self.step + 1, self.rd + 1))

        msg_progress = 'progress: {}/{}\r'
        func = getattr(self, self.func_name, None)
        if func is None:
            raise AttributeError('Given {func} was not defined in {cls}'.format(
                                 func=self.func_name, cls=self.__class__))
        try:
            for i in range(1, self.step+1):
                rlen = len(self.data)*i//self.step
                tlog[i, 0] = rlen
                for r in range(self.rd):
                    st = default_timer()
                    func(self.data[:rlen], *self.args, **self.kwargs)
                    et = default_timer()
                    tlog[i, r+1] = et - st
                self.stream.write(msg_progress.format(i, self.step))
        except:
            raise
        finally:
            self.tear_down()
        return tlog


class MemBenchmarkCase(BenchmarkCase):
    def run(self):
        raise NotImplementedError('MemBenchmarkCase is not implemented yet.')
