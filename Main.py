from Monitoring.CPU_Monitoring import CpuMonitoringThread
from Monitoring.Process_CPU_Monitoring import ProcessCpuMonitoringThread
from Monitoring.Mem_Monitoring import MemMonitoringThread
from Monitoring.Process_Mem_Monitoring import ProcessMemMonitoringThread
import threading
import time
import subprocess

#metodo para pegar os PIDs de todos os processos que estão rodando no sistema
def get_processes_id():
    # Executa o comando 'ps -e' no terminal e captura a saída como uma string
    output = subprocess.check_output(['ps', 'a'])

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
    cpu_cores_info = {}
    # cria uma instância e uma thread da classe CpuMonitoringThread para cada CPU de interesse
    for cpu_core in cpu_cores:
        t = CpuMonitoringThread(cpu_core)
        t.start()
        threads.append(t)

        cpu_cores_info[cpu_core] = t.get_cpu_usage()

    #cria uma instância e uma thread da classe ProcessCpuMonitoringThread verificar o número de threads no sistema
    process_cpu_usage = ProcessCpuMonitoringThread()
    process_cpu_usage.start()


    #dado um determinado processo ele busca infomrações como num_threads atreladas ao process, prioridade do processo, nome do processo e uso da cpu 
    processo = get_processes_id()[145]
    print(f"Processo: {processo} CPU usage: {process_cpu_usage.get_process_cpu_usage(processo)}")

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
        print(threads[0].get_threads_used(get_processes_id()))
        
        #recebe o dicionário com os pids dos processos e os usuário
        '''users = threads[0].get_process_users(get_processes_id())
        unique_users = list(set(users.values())) 
        print(f"Usuários por processo: {unique_users}", end='\n\n') '''

        #recebe o um pid e recebe o usuário do processo
        user = process_cpu_usage.get_process_user(processo)
        print(f"O processo {processo} tem o seguinte usuário {user}", end='\n\n') 

        for t in threads:
            try:
                percent_use = t.get_cpu_usage()
                cpu_cores_info[t.cpu_core] = percent_use

            except:
                print(mem.get_mem_usage(), end='\n')

        print(cpu_cores_info, end='\n\n')
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        
        time.sleep(5)


