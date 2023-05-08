import threading

class ProcessCpuMonitoringThread():

    def get_process_cpu_usage(self, pid):
        
        process_cpu_inf = {}
        # Leitura do arquivo de estatísticas do processo
        with open(f'/proc/{pid}/stat', 'r') as f:
            stat = f.read().split()
        # Tempo total de CPU do processo em jiffies
        utime = int(stat[13])                                   #tempo de CPU gasto em modo usuário (user mode)
        stime = int(stat[14])                                   #tempo de CPU gasto em modo kernel (system mode)
        cutime = int(stat[15])                                  #tempo de CPU gasto em modo usuário pelas threads filhas do processo
        cstime = int(stat[16])                                  #tempo de CPU gasto em modo kernel pelas threads filhas do processo
        process_cpu_inf['num_threads'] = int(stat[19])          #threads que foram criadas para o processo
        process_cpu_inf['priority'] = int(stat[40])             #prioridade do processo (-20 até 19), quanto mais baixo maior a prioridade
        process_cpu_inf['processor'] = int(stat[38])            #ultima cpu que que realizou o processamento do processo
        process_cpu_inf['process_name_limited'] = str(stat[1]).replace("(", "").replace(")", "")  #nome abreviado do processo/programa     

        total_time = utime + stime + cutime + cstime

        # Tempo de clock do sistema em jiffies
        with open('/proc/stat', 'r') as f:
            cpu_stat = f.readline().split()[1:]
        cpu_time = sum(map(int, cpu_stat))
        # Cálculo do uso de CPU do processo em porcentagem
        process_cpu_inf['cpu_usage'] = round((total_time / cpu_time) * 100, 3)

        return process_cpu_inf
    
    def get_process_user(self, pid):
        process_users = {}
        
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
            pass
    
        return process_users 

        

