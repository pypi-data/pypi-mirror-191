import time


def bench_time(function):
    def wrapper(*args, **kwargs):
        before = time.time()
        val = function(*args, **kwargs)
        after = time.time()
        time_diff = after-before
        fname = function.__name__
        print(f"BENCH_TIME: {fname} took {time_diff} seconds to execute")
        return val
    return wrapper
