import windows
import time
browser_proc = windows.Window(path = '/bin/firefox')
browser_proc.open()
time.sleep(1)
#current_proc = browser_proc
print (browser_proc.proc.pid)
current_proc = browser_proc
time.sleep(1)
browser_proc.close()
