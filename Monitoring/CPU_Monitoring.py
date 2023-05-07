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
            
        with open('/proc/stat', 'r') as f:
            for line in f:              
                #verificamos qual linha possui as informações que desejamos
                if line.startswith(self.cpu_core) and line.split()[0] == self.cpu_core:

                    cpu_times = line.split()[1:]
                    
                    #somamos os tempo total de uso da cpu em um segundo instante                    
                    total_cpu_time_end = sum(map(int, cpu_times))
                    #pegamos o tempo oscioso do cpu em um um segundo instante                    
                    idle_time_end = int(cpu_times[3])

                    #verificamos a procentagem de uso total do cpu (tempo ocioso/tempo total de processamento)
                    cpu_usage = 100*(1-((idle_time_end - self.idle_time_init) / (total_cpu_time_end-self.total_cpu_time_init)))
                        
                    # atualizamos as variaveis iniciais, as quais representam o uso da cpu em um primeiro instante (após essa atualização teremos uma média melhor da porcentagem de uso da cpu) 
                    self.total_cpu_time_init = total_cpu_time_end
                    self.idle_time_init = idle_time_end
                    return(f"{self.cpu_core} usage: {cpu_usage:.2f}%")
                    
    def get_threads_used(self, pids):
    
        total_threads = 0

        for pid in pids:
            try:
                with open(f"/proc/{pid}/stat", 'r') as stat_file:
                    stat_content = stat_file.read()
                    #pega o item na possição 19 que representa o número de threads que foram criadas para o processo  
                    num_threads = int(stat_content.split()[19])
                    #soma o número de threads que foram criadas para cada um dos processos
                    total_threads += num_threads
            except:
                continue

        return(f"Total de threads: {total_threads}")
    

    def get_process_users(self, pids):
        process_users = {}
        for pid in pids:
            try:
                with open(f"/proc/{pid}/status", 'r') as status_file:
                    status_content = status_file.readlines()
                    for line in status_content:
                        if line.startswith('Uid:'):
                            #pega o userid do arquivo status
                            uid = int(line.split()[1])
                            with open('/etc/passwd', 'r') as passwd_file:
                                passwd_content = passwd_file.readlines()
                                for passwd_line in passwd_content:
                                    #verifica no arquivo passwd qual usuário possui o pid mapeado para o processo
                                    if int(passwd_line.split(':')[2]) == uid:
                                        username = passwd_line.split(':')[0]
                                        process_users[pid] = username
            except:
                continue
        
        return process_users 

