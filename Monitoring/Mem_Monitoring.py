"""
Mostrar dados globais do uso de memória do sistema, p.ex. percentual de uso da memória,
percentual de memória livre, quantidade de memória física (RAM) e virtual, etc.

"""
import threading
import time

class MemMonitoringThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.mem_total = 0
        self.mem_free = 0
        self.mem_available = 0
        self.cached_mem = 0
        self.virtual_mem = 0        
    
    def get_mem_usage(self):    
        while True:
            with open('/proc/meminfo', 'r') as f:
                for line in f:                    
                    l = line.split()
                    if(l[0] == "MemTotal:"):
                        self.mem_total = int(l[1])/1024
                    if(l[0] == "MemFree:"):
                        self.mem_free = int(l[1])/1024
                    if(l[0] == "MemAvailable:"):
                        self.mem_available = int(l[1])/1024
                    if(l[0] == "Cached:"):
                        self.cached_mem = int(l[1])/1024
                    if(l[0] == "VmallocTotal:"):
                        self.virtual_mem = int(l[1])/1024/1024
                    
                      
            time.sleep(1)
            return ({
                "total": self.mem_total,
                "free": self.mem_free,
                "cached": self.cached_mem,
                "virtual": self.virtual_mem,
                "available": self.mem_available
            })
            
        
        