from Monitoring.CPU_Monitoring import CpuMonitoringThread
from Monitoring.Mem_Monitoring import MemMonitoringThread
from Monitoring.Process_Mem_Monitoring import ProcessMemMonitoringThread
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

#metodo para pegar o número de cores da máquina
def get_number_cores():    
    #abre o arquivo cpuinfo do diretório proc
    with open('/proc/cpuinfo') as f:
        cpuinfo = f.read()
    
    #conta a quantidade de vezes que a palavra processor aparece no arquivo cpuinfo
    num_cores = cpuinfo.count('processor\t:')
    #retorna um inteiro indicando o número de cores que a maquina possui
    return num_cores

if __name__ == '__main__':
    
    cpu_cores = []
    for core in range(0, get_number_cores()):
        cpu_cores.append('cpu'+str(core))
   
    threads = []
    
    # cria uma instância e uma thread da classe CpuMonitoringThread para cada CPU de interesse
    for cpu_core in cpu_cores:
        t = CpuMonitoringThread(cpu_core)
        t.start()
        threads.append(t)

    #cria uma instância e uma thread da classe CpuMonitoringThread verificar o número de threads no sistema
    threads_count = CpuMonitoringThread(cpu_core[0])
    threads_count.start()
    #threads.append(threads_count)

    # cria uma instância da classe MemMonitoringThread
    mem = MemMonitoringThread()
     
    pids = get_processes_id()
    
    for pid in pids:        
        process = ProcessMemMonitoringThread(pid)
        print(f'PID: {pid}\n')
        print(process.get_process_memory_usage())
        
    # loop principal que mostra o uso de CPU

    while True:        
        
        print(f"Processos rodando no sistema: {len(get_processes_id())}")
        print(threads_count.get_threads_used(get_processes_id()))
        
        #recebe o dicionário com os pids dos processos e os usuário
        users = threads_count.get_process_users(get_processes_id())
        unique_users = list(set(users.values())) 
        print(f"Usuários por processo: {unique_users}", end='\n\n')     
             
        for t in threads:
            try:
                print(t.get_cpu_usage(), end='\n')

            except:
                print(mem.get_mem_usage(), end='\n\n')
                time.sleep(5)



