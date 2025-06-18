# This is a script to test the speed of an operation that takes a long time to run.
import time
import psutil
import os

def test_speed():
    print("Starting speed test...")
    print("-" * 50)
    
    # Record start time and memory
    start_time = time.time()
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"Start time: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    print(f"Initial memory usage: {start_memory:.2f} MB")
    print()

    # Run the test
    print("Running test_ADD_small()...")
    from lib.calculator_logic.ADD import test_ADD_small
    test_ADD_small()

    # Record end time and memory
    end_time = time.time()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Calculate metrics
    elapsed_time = end_time - start_time
    memory_used = end_memory - start_memory
    
    print()
    print("-" * 50)
    print("Speed test results:")
    print(f"End time: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
    print(f"Total execution time: {elapsed_time:.4f} seconds")
    print(f"Final memory usage: {end_memory:.2f} MB")
    print(f"Memory increase: {memory_used:.2f} MB")
    print(f"Average time per operation: {elapsed_time:.6f} seconds")

if __name__ == "__main__":
    test_speed()
    print("All tests passed!")