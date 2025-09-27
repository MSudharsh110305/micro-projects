import time
import threading
import multiprocessing
import asyncio

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def run_with_threads(n, num_threads):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=fibonacci, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def run_with_multiprocessing(n, num_processes):
    processes = []
    for _ in range(num_processes):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

async def run_with_asyncio(n, num_tasks):
    tasks = []
    for _ in range(num_tasks):
        tasks.append(asyncio.create_task(async_fibonacci(n)))
    await asyncio.gather(*tasks)

async def async_fibonacci(n):
    return fibonacci(n)

def measure_time(func, *args):
    start_time = time.time()
    func(*args)
    return time.time() - start_time

if __name__ == '__main__':
    n = 40
    num_threads = 4
    num_processes = 4
    num_tasks = 4

    thread_time = measure_time(run_with_threads, n, num_threads)
    print(f"Time with threads: {thread_time:.2f} seconds")

    multiprocessing_time = measure_time(run_with_multiprocessing, n, num_processes)
    print(f"Time with multiprocessing: {multiprocessing_time:.2f} seconds")

    asyncio_time = measure_time(asyncio.run, run_with_asyncio(n, num_tasks))
    print(f"Time with asyncio: {asyncio_time:.2f} seconds")
