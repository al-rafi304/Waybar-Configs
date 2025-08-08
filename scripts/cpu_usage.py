import os
import time
import psutil

save_file = '/tmp/cpu.txt'

def get_cpu_usage():
    with open("/proc/stat", "r") as f:
        cpu_stats = f.readline().split()[1:8]
    
    cpu_stats = list(map(int, cpu_stats))
    total_time = sum(cpu_stats)
    idle_time = cpu_stats[3]

    return total_time, idle_time

def get_past_cpu_usage():
    with open(save_file, "r") as f:
        cpu_stats = f.readline().split()[1:8]
    
    cpu_stats = list(map(int, cpu_stats))
    total_time = sum(cpu_stats)
    idle_time = cpu_stats[3]

    return total_time, idle_time

def save_cpu_usage():
    with open("/proc/stat", "r") as f:
        cpu_stats = f.read()
        
    with open(save_file, 'w') as f:
        f.write(cpu_stats)

def get_cpu_percent():

    if not os.path.exists(save_file):
        save_cpu_usage()
        # print(0)
        return 1

    # Get initial values
    prev_total, prev_idle = get_past_cpu_usage()

    # Sleep for a short interval (e.g., 0.1s) to calculate CPU usage over time
    # time.sleep(interval)

    # Get new values after sleep
    total, idle = get_cpu_usage()

    # Calculate CPU usage percentage
    delta_total = total - prev_total
    delta_idle = idle - prev_idle

    cpu_usage = round((1.0 - delta_idle / delta_total) * 100)

    # print(cpu_usage)
    save_cpu_usage()
    return cpu_usage
    print(f"CPU Usage: {cpu_usage:.2f}%")

# get_cpu_percent()