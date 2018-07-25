# nac: it's "not a chair", it's a bench
Write your microbenchmark scripts in a unittest-like way.

## Requirement
* numpy >= 1.9.1
* matplotlib >= 1.4.2

## Installation
`cd` to this directory, and then
```shell
$ python setup.py install
```

## Usage
0. Suggested structure of your project
```
your_project/
    run_bench.py    # the script to run benchmark
    mod_foo/
        ...
        benchmarks/         # the directory where your files of benchmark cases locate
            bench_foo.py
```

1. Write your microbenchmark case
```python
# bench_foo.py
import numpy as np
from nac import BenchmarkCase

# --- Functions for demonstration, you should import functions from your module. ----
# --- These 2 functions do the same thing, but take input parameters in different order. ---
def mul_data_mask(data, mask):
    return data*mask

def mul_mask_data(mask, data):
    return data*mask

# --- Define a benchmark case ---
class BenchFoo(BenchmarkCase):
    def set_up(self):
        # Initialize your data (which will be partitioned into several parts, and the size
        # of each part is determined by `step`)
        self.data = np.ones(1000, dtype=float)

        # Set parameters for benchmark
        # In this case, we set up a loop that runs 100 times, 3 round in each run.
        self.step = 100     # number of times that loop runs
        self.rd = 3         # number of times that loop repeated in one 

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

```

2. Write a script to run benchmark
```python
# run_bench.py
from nac import BenchmarkLoader, BenchmarkRunner, LogPlotter

def main():
    loader = BenchmarkLoader()
    suite = loader.discover('.')
    BenchmarkRunner.run_benchmark_suite(suite)

    # Plot result of benchmark
    plotter = LogPlotter('bench_log', 'Bench*.csv')
    plotter.plot()

if __name__ == '__main__':
    main()

```

3. Run benchmark
```shell
$ cd your_project
$ python run_bench.py
```
