"""
Mostrar dados globais do uso de memória do sistema
"""
class MemMonitoring():
    def __init__(self):
        super().__init__()
              
    
    def get_mem_usage(self):    
        mem_total = 0
        mem_free = 0
        mem_available = 0
        cached_mem = 0
        virtual_mem = 0 
        #usar o comando open para abrir o arquivo meminfo da pasta /proc
        with open('/proc/meminfo', 'r') as f:
            for line in f:                              #um for percorrendo cada linha do arquivo
                l = line.split()                        #vai transformar cada linha em um array
                if(l[0] == "MemTotal:"):                #vai checar o primeiro indice do array de cada linha
                    mem_total = int(l[1])/1024     #atribuir o valor indicado
                if(l[0] == "MemFree:"):
                    mem_free = int(l[1])/1024
                if(l[0] == "MemAvailable:"):
                    mem_available = int(l[1])/1024
                if(l[0] == "Cached:"):
                    cached_mem = int(l[1])/1024
                if(l[0] == "VmallocTotal:"):
                    virtual_mem = int(l[1])/1024/1024
                
                    
        #retornar um dicionario que sera usado no dashboard
        return ({
            "total": mem_total,
            "free": mem_free,
            "cached": cached_mem,
            "virtual": virtual_mem,
            "available": mem_available
        })
            
        
        