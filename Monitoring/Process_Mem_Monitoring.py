"""
2. Mostrar informações detalhadas sobre o uso de memória para cada processo, p.ex. quantidade
total de memória alocada, quantidade de páginas de memória (total, de código, heap, stack),
etc.
3. Ao mostrar informações detalhadas de cada processo, as informações podem ser apresentadas
em uma nova tela (ou aba) que, ao ser fechada, retorna a tela principal
"""

import threading
import time
import subprocess


class ProcessMemMonitoringThread(threading.Thread):
    def __init__(self, pid):
        super().__init__()
        self.pid = pid
        self.size_total = 0
        self.pss_total = 0
        self.rss_total = 0
    
    def get_process_memory_usage(self):
        try:
            with open(f'/proc/{self.pid}/smaps', 'r') as f:
                for line in f:                    
                    l = line.split()
                    if(l[0] == "Size:"):
                            self.size_total += int(l[1])/1024
                    if(l[0] == "Pss:"):
                        self.pss_total += int(l[1])/1024
                    if(l[0] == "Rss:"):
                        self.rss_total += int(l[1])/1024
        except Exception as e: print(e)
        
        return (f'Size: {self.size_total:.2f}Mb\nPss: {self.pss_total:.2f}Mb\nRss: {self.rss_total:.2f}Mb\n')

                         
        
        