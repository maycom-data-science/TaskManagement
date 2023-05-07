"""
Mostrar informações detalhadas sobre o uso de memória para cada processo
"""

class ProcessMemMonitoring():
    def __init__(self):
        super().__init__()     
        
    
    def get_process_memory_usage(self, pid):
        size_total = 0
        pss_total = 0
        rss_total = 0
        try:
            #usar o comando open para abrir o arquivo smaps da pasta /proc/{pid}
            with open(f'/proc/{pid}/smaps', 'r') as f:
                for line in f:                                      #um for percorrendo cada linha do arquivo
                    l = line.split()                                #vai transformar cada linha em um array
                    if(l[0] == "Size:"):                            #vai checar o primeiro indice do array de cada linha
                            size_total += int(l[1])/1024       #atribuir o valor indicado
                    if(l[0] == "Pss:"):
                        pss_total += int(l[1])/1024
                    if(l[0] == "Rss:"):
                        rss_total += int(l[1])/1024
        except Exception as e: print(e)                             #dependendo do processo pode dar erro ao tentar abrir o arquivo
        
        return({
            'size': size_total,
            'pss': pss_total,
            'rss': rss_total
        })
                         
        
        