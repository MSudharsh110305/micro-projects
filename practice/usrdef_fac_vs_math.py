import math
import time

def factorial(n):
    result = 1
    
    for i in range(1, n + 1):
        result *= i
    
    return result

def measure_time(factorial_func, n):
    start_time = time.time()
    factorial_func(n)
    end_time = time.time()
    return end_time - start_time

n = 99999

custom_time = measure_time(factorial, n)
print(f"Custom factorial took {custom_time:.6f} seconds")

builtin_time = measure_time(math.factorial, n)
print(f"Built-in factorial took {builtin_time:.6f} seconds")

if custom_time < builtin_time:
    print("Custom factorial is faster.")
else:
    print("Built-in factorial is faster.")
