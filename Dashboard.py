from Monitoring.CPU_Monitoring import CpuMonitoringThread
from Monitoring.Mem_Monitoring import MemMonitoring
from Monitoring.Process_Mem_Monitoring import ProcessMemMonitoring
import subprocess
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

app = Dash(__name__)

#metodo para pegar o número de cores da máquina
def get_number_cores():    
    #abre o arquivo cpuinfo do diretório proc
    with open('/proc/cpuinfo') as f:
        cpuinfo = f.read()
    
    #conta a quantidade de vezes que a palavra processor aparece no arquivo cpuinfo
    num_cores = cpuinfo.count('processor\t:')
    #retorna um inteiro indicando o número de cores que a maquina possui
    return num_cores


cpu_cores = []
#cria uma lista com o nome de cada um dos nucleos do cpu
number_cores = get_number_cores()              
for core in range(0, number_cores):
    cpu_cores.append('cpu'+str(core))
cpu_cores.append('cpu')

threads = []
cpu_cores_info = []  #primeira possição tem o uso do core 0, a segunda tem o uso do core 1, a terceira o uso do core 2, e a ultima o uso geral da cpu...

# Inicializa as threads de uso da cpu
for cpu_core in cpu_cores:
    t = CpuMonitoringThread(cpu_core)
    t.start()
    threads.append(t)
    cpu_cores_info = t.get_cpu_usage()

#-------------------------------------------

#variavel que vamos usar de "banco de dados" para utilizar no nosso dashboard
database = {
    'index': [],
    'total_memory': 0,
    'free_memory': [],
    'available_memory': [],
    'free_memory_percentual': 0,
    'available_memory_percentual': 0,
    'cached_memory': [],
    'virtual_memory': [],
    'process_size': 0,
    'process_pss': 0,
    'process_rss': 0,
    'cpu_usage': [], #primeira possição tem o uso da cpu 0, a segunda o uso da cpu1, etc... e o ultima possição tem o uso geral da cpu
    'number_threads': 0
}

mem = MemMonitoring()
process_mem = ProcessMemMonitoring()

N = 20

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
#-------------------------

#variavel que vamos usar de "banco de dados" para utilizar no nosso dashboard
database = {
    'index': [],
    'total_memory': 0,
    'free_memory': [],
    'available_memory': [],
    'free_memory_percentual': 0,
    'available_memory_percentual': 0,
    'cached_memory': [],
    'virtual_memory': [],
    'process_size': [],
    'process_pss': [],
    'process_rss': [],
    'number_threads': [],
    'cpu_usage': [],
    'process_users': []
}

processes = get_processes_id()


#HTML do nosso dashboard
app.layout = html.Div(
    children=[
        dcc.Interval(id='interval', interval= 5000),
        html.Div(id='memory_info'),   
        dcc.Checklist(
            id='memory_check_list',
            options=[
                {'label': 'Memória Disponivel', 'value': 'available_memory'},
                {'label': 'Memória Livre', 'value': 'free_memory'},
                {'label': 'Memória em Cache', 'value': 'cached_memory'}
            ],
            value=['available_memory']
        ),       
        dcc.Graph(
            id='memory_graph',
            config={'displayModeBar': False},
        ),
        html.Div(id='cpu_info'),   
        dcc.Graph(
            id='CPU_graph',
            config={'displayModeBar': False}
        ),
        dcc.Dropdown(
            id = 'process_dropdown',
            options = processes,
            value= processes[0]
        ),
        html.Div(id='process_memory_info'),        
        dcc.Graph(
            id='process_memory_graph',
            config={'displayModeBar': False},
        ),
       
    ]
)



#Função que chama a função do arquivo Mem_Monitoring.py, get_mem_usage(), para pegar os dados de memoria do sistema e atualizar na nossa variavel 'database'
def update_memory_data(value):
    mem_data = mem.get_mem_usage() #pega os dados da função de Mem_Monitoring.py
    database['index'].append(value)
    database['total_memory'] = mem_data['total']
    database['free_memory'].append(mem_data['free'])
    database['free_memory_percentual'] = mem_data['free']/mem_data['total']*100
    database['available_memory'].append(mem_data['available'])
    database['available_memory_percentual'] = mem_data['available']/mem_data['total']*100
    database['cached_memory'].append(mem_data['cached'])
    database['virtual_memory'].append(mem_data['virtual'])

def update_cpu_data(value):
    
    new_cpu_data = []
    for t in threads:
        new_cpu_data.append(t.get_cpu_usage())

    database['cpu_usage'] = new_cpu_data
    #print(database['cpu_usage'][0])

    database['number_threads'] = threads[0].get_threads_used(get_processes_id())

    users = threads[0].get_process_users(get_processes_id())
    unique_users = list(set(users.values())) 
    database['process_users'] = unique_users 



def update_process_memory_data(pid):
    process_data = process_mem.get_process_memory_usage(pid)
    database['process_size'] = process_data['size']
    database['process_pss'] = process_data['pss']
    database['process_rss'] = process_data['rss']


#chama a função para atualizar os dados de memoria a cada 5 segundos
@app.callback(
    Output('memory_info', 'children'), 
    Input('interval', 'n_intervals'),
)
def update_total_memory(n_intervals):
    update_memory_data(n_intervals)
    #update_cpu_data(n_intervals) 
    return (f'Memória: Total: {database["total_memory"]:.2f}Mb_____Disponivel: {database["available_memory"][-1]:.2f}Mb ({database["available_memory_percentual"]:.2f}%)_____Livre: {database["free_memory"][-1]:.2f}Mb ({database["free_memory_percentual"]:.2f}%)_____Em cache: {database["cached_memory"][-1]:.2f}Mb_____Virtual: {database["virtual_memory"][-1]:.2f}Gb')

#chama a funcao para atualizar o grafico de memoria a cada 5 segundos
@app.callback(
    Output('memory_graph', 'figure'),
    [Input('memory_check_list', 'value'),
    Input('interval', 'n_intervals')]
)
def update_memory_graph(input_data, n_intervals):
    
    graph = {
        'data': [],
        'layout': {
            'title': 'Uso de Memoria em Mb',
            'height': 400,
            'width': 600,
        }
    }
    for x in input_data:
        #input_data é o nome do grafico que ele vai mostrar
        graph['data'].append(
            {

                'y': database[x][-N:], #pega a variavel do grafico que ele quer mostrar e bota no eixo y do grafico
                'x': database['index'][-N:], #index, contabilizacao de "tempo", no eixo x
                'name': x,                
            },
        )
    return graph

@app.callback(
    Output('cpu_info', 'children'), 
    Input('interval', 'n_intervals'),
)

def update_cpu_info(n_intervals):
    update_cpu_data(n_intervals) 
    return (f'Número total de processos no sistema: {len(get_processes_id())}_____Numero de threads criadas: {database["number_threads"]}___Usuários dos processos em exec({database["process_users"]}%)_____Uso geral da CPU: {database["cpu_usage"][-1]:.2f}%')


@app.callback(
    Output('CPU_graph', 'figure'),
    Input('interval', 'n_intervals')

)
def update_cpu_graph(n_intervals):
    graph = {
        'data': [],
        'layout': {
            'title': 'Uso de CPU em %',
            'height': 400,
            'width': 600,
        }
    }
    print(database['cpu_usage'])
    graph['data'].append(
        {
            'x': cpu_cores,
            'y': database['cpu_usage'],
            'name': "Grafico CPU",
            'type': 'bar',
        }
    )
   
    return graph

#chama a função para atualizar a lista de processos a cada 5 segundos
@app.callback(
    Output("process_dropdown", "options"),
    Input('interval', 'n_intervals')
)
def update_process_options(n_intervals):
    processes = get_processes_id()
    return processes

#chama a função para atualizar os dados de memoria do processo a cada 5 segundos
@app.callback(
    Output('process_memory_info', 'children'), 
    [Input('process_dropdown', 'value'),
    Input('interval', 'n_intervals')]
)
def update_total_memory(process, n_intervals):
    update_process_memory_data(process)    
    return (f'Tamanho: {database["process_size"]:.2f}Mb_____Pss: {database["process_pss"]:.2f}Mb _____Rss: {database["process_rss"]:.2f}Mb')

#chama a funcao para atualizar o grafico de memoria do processo a cada 5 segundos
@app.callback(
    Output('process_memory_graph', 'figure'),
    [Input('process_memory_info', 'children') ]
)
def update_process_memory_graph(value):
    
    graph = {
        'data': [],
         'layout': {
            'title': 'Uso de Memória do Processo em Mb',
            'height': 400,
            'width': 300,
        }
    }
    
    #input_data é o nome do grafico que ele vai mostrar
    graph['data'].append(
        {
            'y': [database['process_size'], database['process_pss'], database['process_rss']][-N:], #pega a variavel do grafico que ele quer mostrar e bota no eixo y do grafico
            'x': ['Size', 'Pss', 'Rss'][-N:], #index, contabilizacao de "tempo", no eixo x
            'type': 'bar',
        }
    )
        
    return graph

app.run_server(debug=True)
