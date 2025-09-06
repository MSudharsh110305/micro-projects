import time
from functools import wraps

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        args_preview = args[1:] if args else ()
        print(f"[LOG] {func.__name__} args={args_preview} kwargs={kwargs} took={elapsed_ms:.2f}ms")
        return result
    return wrapper
