import multiprocessing
import psutil
import time
import runpy
import sys

def run_script():
    # Temporarily replace sys.argv with the args you want
    original_argv = sys.argv
    sys.argv = ["main2PG_condor.py", "10", "0.5", "1"]

    try:
        # This will run the script as if it were the main program
        runpy.run_path("main2PG_condor.py", run_name="__main__")
    finally:
        # Restore the original sys.argv after running the script
        sys.argv = original_argv

if __name__ == "__main__":
    # Start the script in a separate process
    p = multiprocessing.Process(target=run_script)
    p.start()

    ps_process = psutil.Process(p.pid)
    peak_memory = 0
    memory_sum = 0  # Sum of all memory readings
    count = 0  # Number of memory readings taken

    try:
        while True:
            # Check if process has terminated
            if not p.is_alive():
                break
            memory_info = ps_process.memory_info()
            current_memory = memory_info.rss  # Resident Set Size in bytes
            peak_memory = max(peak_memory, current_memory)
            memory_sum += current_memory
            count += 1
            time.sleep(0.1)  # Sleep to avoid busy waiting
    except psutil.NoSuchProcess:
        pass
    finally:
        p.join()  # Ensure the process finishes

    if count > 0:  # To avoid division by zero
        average_memory = memory_sum / count
        print(f"Peak memory usage: {peak_memory / 1024 ** 2:.2f} MB")
        print(f"Average memory usage: {average_memory / 1024 ** 2:.2f} MB")
    else:
        print("No memory usage data collected.")