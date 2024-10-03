import threads
import time
import pandas as pd

threads.start_monitor()

loads = {}
loads["1s"] = []
loads["2s"] = []
loads["5s"] = []
marker = time.time()
while time.time() - marker < 10:
    time.sleep(1)
    for i in [1, 2, 5]:
        loads[f"{i}s"].append(threads.cpu_average(i))

df = pd.DataFrame(loads)
print(df.head())
