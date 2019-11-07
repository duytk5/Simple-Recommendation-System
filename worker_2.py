from module import Module
import time

mo = Module()
time_update = 10

while True:
    print (mo.update())
    time.sleep(time_update)
