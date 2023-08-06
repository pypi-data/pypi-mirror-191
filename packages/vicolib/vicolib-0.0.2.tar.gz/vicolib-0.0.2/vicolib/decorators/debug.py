from vicolib.converter.time import Time
from functools import wraps


# Prints the return of a function with timestamp and function name
def debug(function):
    def wrapper(*args, **kwargs):
        val = function(*args, **kwargs)
        timestamp = Time.stamp_now()
        function_name = function.__name__
        log = f"[{timestamp}]: {function_name} -> {val}"
        print(log)
        return val

    return wrapper


# Prints the return like @debug but with a line of "*" (or the given char) before and after, so it really stands out
def create_important_decorator(char="!"):
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            val = function(*args, **kwargs)
            timestamp = Time.stamp_now()
            function_name = function.__name__
            log = f"[{timestamp}]: {function_name} -> {val}"
            print(len(log) * char)
            print(log)
            print(len(log) * char)
            return val

        return wrapper

    return decorate


# Returns Default important decorator (char="!")
important = create_important_decorator()