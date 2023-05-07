from Monitoring.CPU_Monitoring import CpuMonitoringThread
from Monitoring.Mem_Monitoring import MemMonitoringThread
from Monitoring.Process_Mem_Monitoring import ProcessMemMonitoringThread
import subprocess
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


app = Dash(__name__)
mem = MemMonitoringThread()

N = 20

database = {
    'index': [],
    'total_memory': 0,
    'free_memory': [],
    'available_memory': [],
    'free_memory_percentual': 0,
    'available_memory_percentual': 0,
    'cached_memory': [],
    'virtual_memory': [],
}


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
        )
    ]
)

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

def update_memory_data(value):
    mem_data = mem.get_mem_usage() #pega os dados da função de Mem_Monitoring
    database['index'].append(value)
    database['total_memory'] = mem_data['total']
    database['free_memory'].append(mem_data['free'])
    database['free_memory_percentual'] = mem_data['free']/mem_data['total']*100
    database['available_memory'].append(mem_data['available'])
    database['available_memory_percentual'] = mem_data['available']/mem_data['total']*100
    database['cached_memory'].append(mem_data['cached'])
    database['virtual_memory'].append(mem_data['virtual'])


@app.callback(
    Output('memory_info', 'children'), 
    Input('interval', 'n_intervals'),
)
def update_total_memory(n_intervals):
    update_memory_data(n_intervals)
    return f'Memória: Total: {database["total_memory"]:.2f}_____Livre: {database["free_memory"][-1]:.2f} ({database["free_memory_percentual"]:.2f}%)_____Em cache: {database["cached_memory"][-1]:.2f}_____Virtual: {database["virtual_memory"][-1]:.2f}'

@app.callback(
    Output('memory_graph', 'figure'),
    Input('memory_check_list', 'value')
    
)
def update_memory_graph(input_data):
    
    graph = {
        'data': []
    }
    for x in input_data:

        graph['data'].append(
            {
                'Valor': database[x][-20:],
                'Tempo': database['index'][-20:],
                'name': "Grafico Memória",
                'type': 'line'
            },
        )
    return graph

app.run_server(debug=True)