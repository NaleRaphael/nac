from __future__ import absolute_import, division
import numpy as np

from nac.core import BenchmarkCase, TimeBenchmarkCase


class FakeStream(object):
    def write(self, *args, **kwargs):
        """ Do nothing in unit test stage. """
        pass


class EmptyCase(BenchmarkCase):
    """ A case do nothing """
    pass


class TimeArrayMultiplication(TimeBenchmarkCase):
    func_list = ['time_foo', 'time_bar']

    def set_up(self):
        self.stream = FakeStream()
        self.enable_logging = False
        self.data = np.ones(100, dtype='float')
        self.args = ()
        self.kwargs = {}
        self.step = 10
        self.rd = 3

    def time_foo(self, data, *args, **kwargs):
        foo(data, np.array([2.0]))

    def time_bar(self, data, *args, **kwargs):
        bar(np.array([2.0]), data)


# ----- Functions with different order of input parameters -----
def foo(data, mask):
    return data*mask

def bar(mask, data):
    return data*mask
