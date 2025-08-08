import psutil
import os
import json
from cpu_usage import get_cpu_percent

brail = [
    ['⢀','⢀','⢠','⢰','⢸'],
    ['⡀','⣀','⣠','⣰','⣸'],
    ['⡀','⣄','⣤','⣴','⣼'],
    ['⡀','⣆','⣦','⣶','⣾'],
    ['⡀','⣇','⣧','⣷','⣿'],
]

graph_file = '/tmp/cpu_out.txt'
last_cpu_file = '/tmp/last_cpu.txt'


# Creating file if doesn't exist
if not os.path.exists(graph_file):
    with open(graph_file, "w") as f:
        f.write("        ")
if not os.path.exists(last_cpu_file):
    with open(last_cpu_file, "w") as f:
        f.write("0")

with open(last_cpu_file, 'r') as f:
    last = int(f.readlines()[0])

# cpu = psutil.cpu_percent(0.1)
cpu = get_cpu_percent()
cpu4 = round(cpu*4/100)

status = ''
status += brail[last][cpu4]

# print(brail[last][cpu4], end='')
last = cpu4

with open(graph_file, 'a') as f:
    f.write(status)
with open(last_cpu_file, 'w') as f:
    f.write(str(last))

with open(graph_file, 'r') as f:
    graph = f.readline()[-6:]
# print(str(cpu) + '%')

out = {
    'text': f"{round(cpu)}",
    'alt': f"{graph}"
}
# out = {
#     'format-alt': f"{round(cpu)}%",
#     'text': graph
# }

print(json.dumps(out))