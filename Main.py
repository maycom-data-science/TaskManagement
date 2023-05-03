from Monitoring.CPU_Monitoring import CpuMonitoringThread
from Monitoring.Mem_Monitoring import MemMonitoringThread
import threading
import time
import subprocess

#metodo para pegar os PIDs de todos os processos que estão rodando no sistema
def get_processes_id():
    # Executa o comando 'ps -e' no terminal e captura a saída como uma string
    output = subprocess.check_output(['ps', '-e'])

    pids = []
    for line in output.splitlines():
        # Divide a linha em campos e extrai o PID do primeiro campo
        fields = line.split()        
        if fields[0].isdigit():
            pid = int(fields[0])
            pids.append(pid)

    # retorna array de PIDs
    return(pids)

if __name__ == '__main__':
    cpu_cores = ['cpu']#, 'cpu0', 'cpu1', 'cpu2', 'cpu3', 'cpu4', 'cpu5', 'cpu6', 'cpu7', 'cpu8', 'cpu9', 'cpu10', 'cpu11']  # lista com os nomes das CPUs de interesse
    threads = []
    
    #print(get_processes_id())
    # cria uma instância da classe CpuMonitoringThread para cada CPU de interesse
    for cpu_core in cpu_cores:
        t = CpuMonitoringThread(cpu_core)
        t.start()
        threads.append(t)

     # cria uma instância da classe MemMonitoringThread
    mem = MemMonitoringThread()
    mem.start()
    threads.append(mem)
    
    # loop principal que mostra o uso de CPU
    while True:        
        for t in threads:
            try:
                print(t.get_cpu_usage(), end='\n\n')                
            except:
                print(mem.get_mem_usage(), end='\n\n')


