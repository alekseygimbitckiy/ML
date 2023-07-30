import csv
import pandas as pd
df = pd.read_csv('data.csv')
df_0 = pd.read_csv('out_6.csv')

dataset = pd.concat([df, df_0])
print (dataset.head)

dataset.to_csv('data.csv')
# import subprocess
# import time
# browser_proc = subprocess.Popen('/bin/firefox')
# print (browser_proc.pid)
# time.sleep(5)
# browser_proc.terminate()
# time.sleep(5)
# if browser_proc.poll() is None:
#     browser_process.kill()


