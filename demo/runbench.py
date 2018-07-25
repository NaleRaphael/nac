from nac import BenchmarkLoader, BenchmarkRunner
from nac.plotter import LogPlotter

def main():
    loader = BenchmarkLoader()
    suite = loader.discover('.')
    runner = BenchmarkRunner()
    runner.run_benchmark_suite(suite)

    # Plot result of benchmark
    plotter = LogPlotter('bench_log', 'Bench*.csv')
    plotter.plot()

if __name__ == '__main__':
    main()
