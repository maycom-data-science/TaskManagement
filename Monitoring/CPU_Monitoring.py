"""
1. Monitorar e apresentar as características e propriedades de todos os processes existentes
em execução no sistema operacional;

1. Mostrar dados globais do uso do processador, p.ex. percentual de uso do processador, percentual de tempo ocioso, quantidade total de processos e threads, etc.
2. Mostrar a lista de processos existentes juntamente com os respectivos usuários;
3. Mostrar informações sobre os threads de cada processo;
4. Mostrar informações detalhadas de cada processo. Nesse caso, as informações podem ser apresentadas em uma nova tela (ou aba) que, ao ser fechada, retorna a tela principal.
"""
import threading
import time

class CpuMonitoringThread(threading.Thread):
    def __init__(self, cpu_core):
        super().__init__()
        self.cpu_core = cpu_core
        self.total_cpu_time_init = 0
        self.idle_time_init = 0
    
    def get_cpu_usage(self):
        while True:    
            with open('/proc/stat', 'r') as f:
                for line in f:
                    
                    if line.startswith(self.cpu_core) and line.split()[0] == self.cpu_core:
                        cpu_times = line.split()[1:]
                        self.total_cpu_time_init = sum(map(int, cpu_times))
                        self.idle_time_init = int(cpu_times[3])
                        
                        time.sleep(1)

                        with open('/proc/stat', 'r') as f:
                            line2 = f.readline()

                        cpu_times_2 = line2.split()[1:]
                        total_cpu_time_end = sum(map(int, cpu_times_2))
                        idle_time_end = int(cpu_times_2[3])

                        cpu_usage = 100*(1-((idle_time_end - self.idle_time_init) / (total_cpu_time_end-self.total_cpu_time_init)))
                        
                        self.total_cpu_time_init = total_cpu_time_end
                        self.idle_time_init = idle_time_end
                        return(f"{self.cpu_core} usage: {cpu_usage:.2f}%")
                        
