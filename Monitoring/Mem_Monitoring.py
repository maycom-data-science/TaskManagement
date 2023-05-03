"""
2. Monitorar e apresentar as informações do uso de memória dos processos;
Este objetivo consiste em fornecer as informações de uso de memória global do
sistema e de cada processo individualmente. Os requisitos abaixo devem ser obrigatoriamente
seguidos:
1. Mostrar dados globais do uso de memória do sistema, p.ex. percentual de uso da memória,
percentual de memória livre, quantidade de memória física (RAM) e virtual, etc.
2. Mostrar informações detalhadas sobre o uso de memória para cada processo, p.ex. quantidade
total de memória alocada, quantidade de páginas de memória (total, de código, heap, stack),
etc.
3. Ao mostrar informações detalhadas de cada processo, as informações podem ser apresentadas
em uma nova tela (ou aba) que, ao ser fechada, retorna a tela principal
"""
import threading
import time

class MemMonitoringThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.mem_total = 0
        self.mem_free = 0
        self.ram_mem = 0
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
                    if(l[0] == "Cached:"):
                        self.ram_mem = int(l[1])/1024
                    if(l[0] == "VmallocTotal:"):
                        self.virtual_mem = int(l[1])/1024/1024
                    
            mem_free_percentual = self.mem_free/self.mem_total*100
            
            time.sleep(1)
            return (f'Memoria total: {self.mem_total:.2f}Mb\nMemoria livre: {self.mem_free:.2f}Mb\nPercentual de memoria livre: {mem_free_percentual:.2f}%\nMemoria fisica: {self.ram_mem:.2f}Mb\nMemoria virtual: {self.virtual_mem:.2f}Gb')
            
        
        