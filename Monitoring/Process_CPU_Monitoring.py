"""
1. Uso de CPU de cada processo
2.  
"""
import threading
import math
import time

class ProcessCpuMonitoringThread(threading.Thread):

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

        with open(f"/proc/{pid}/cmdline", "rb") as f:
            #como o conteúdo do arquivo é uma sequência de bytes usamos o metodo read() com decode utf-8 para ler o arquivo, 
            #o rstrip é utilizado apenas para tirar o os demais caracteres a direita da string, os quais não nos interessam
            #Obs: apenas aparece o nome completo do processo/programa se o mesmo ainda estiver ativo
            process_cpu_inf['process_name_active'] = f.read().rstrip(b"\x00").decode("utf-8")
            

        total_time = utime + stime + cutime + cstime

        # Tempo de clock do sistema em jiffies
        with open('/proc/stat', 'r') as f:
            cpu_stat = f.readline().split()[1:]
        cpu_time = sum(map(int, cpu_stat))
        # Cálculo do uso de CPU do processo em porcentagem
        process_cpu_inf['cpu_usage'] = round((total_time / cpu_time) * 100, 2)

        return process_cpu_inf

        

