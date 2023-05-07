"""
Mostrar dados globais do uso de memória do sistema
"""
class MemMonitoring():
    def __init__(self):
        super().__init__()
        self.mem_total = 0
        self.mem_free = 0
        self.mem_available = 0
        self.cached_mem = 0
        self.virtual_mem = 0        
    
    def get_mem_usage(self):    
            #usar o comando open para abrir o arquivo meminfo da pasta /proc
            with open('/proc/meminfo', 'r') as f:
                for line in f:                              #um for percorrendo cada linha do arquivo
                    l = line.split()                        #vai transformar cada linha em um array
                    if(l[0] == "MemTotal:"):                #vai checar o primeiro indice do array de cada linha
                        self.mem_total = int(l[1])/1024     #atribuir o valor indicado
                    if(l[0] == "MemFree:"):
                        self.mem_free = int(l[1])/1024
                    if(l[0] == "MemAvailable:"):
                        self.mem_available = int(l[1])/1024
                    if(l[0] == "Cached:"):
                        self.cached_mem = int(l[1])/1024
                    if(l[0] == "VmallocTotal:"):
                        self.virtual_mem = int(l[1])/1024/1024
                    
                      
           #retornar um dicionario que sera usado no dashboard
            return ({
                "total": self.mem_total,
                "free": self.mem_free,
                "cached": self.cached_mem,
                "virtual": self.virtual_mem,
                "available": self.mem_available
            })
            
        
        