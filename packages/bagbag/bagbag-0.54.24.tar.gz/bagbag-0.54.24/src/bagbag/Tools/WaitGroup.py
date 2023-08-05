
try:
    from .Lock import Lock
except:
    from Lock import Lock

import time

class WaitGroup():
    def __init__(self):
        self.count = 0
        self.lock = Lock()
    
    def Add(self):
        self.lock.Acquire()
        self.count += 1
        self.lock.Release()
    
    def Done(self):
        self.lock.Acquire()
        self.count -= 1
        self.lock.Release()
    
    def Wait(self, timeout:int=-1) -> bool:
        waitedsec = 0 
        while True:
            if self.count == 0:
                return True
            else:
                if timeout != -1 and waitedsec >= timeout:
                    return False 
                time.sleep(1)
                waitedsec += 1