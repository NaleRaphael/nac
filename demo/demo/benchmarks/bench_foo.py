import numpy as np
from nac import BenchmarkCase

# Import your functions to be benchmarked
from demo import (mul_data_mask, mul_mask_data)


# --- Define a benchmark case ---
class BenchFoo(BenchmarkCase):
    def set_up(self):
        # Initialize your data (which will be partitioned into several parts, and the size
        # of each part is determined by `step`)
        self.data = np.ones(1000, dtype=float)

        # Set parameters for benchmark
        # In this case, we set up a loop that runs 100 times, 3 round in each run.
        self.step = 100     # number of times that loop runs
        self.rd = 3         # number of times that loop repeated in one run

        # If you don't want to save the result of benchmark...
        # self.enable_logging = False

        # Declare the other parameters that will be used in each functions to be benchmarked
        self.mask = np.array([2.0])

    # NOTICE:
    # 1. Prefix of the name of each function to be benchmarked should be `time_`.
    # 2. You should at least declare `self` and `data` in a function signature.
    #    e.g.
    #        good: `time_foo(self, data)`, `time_foo(self, data, *args, **kwargs)`
    #        bad:  `time_foo(self)`
    # Then, you can decide the position of the data to be passed into function.
    def time_mul_data_mask(self, data):
        mul_data_mask(data, self.mask)
        # WARNING: Don't pass `self.data` into your function directly!
        # -> mul_data_mask(self.data, self.mask)   # bad!!!

    def time_mul_mask_data(self, data):
        mul_mask_data(self.mask, data)
