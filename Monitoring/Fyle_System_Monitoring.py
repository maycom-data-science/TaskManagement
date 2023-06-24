import subprocess

class FileSystemMonitoring():
    def __init__(self):
        super().__init__()
              
              
    def get_filesystem_info(self, cmd):
        try:
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
            output, _ = process.communicate()

            if process.returncode == 0:
                filesystem_info = []

                # Ignorar a primeira linha do cabeçalho
                lines = output.strip().split('\n')[1:]

                for line in lines:
                    fields = line.split()
                    filesystem = fields[0]
                    type = fields[1]
                    size = fields[2]
                    used = fields[3]
                    available = fields[4]
                    percent_used = fields[5]
                    mountpoint = fields[6]

                    filesystem_info.append({
                        'filesystem': filesystem,
                        'type': type,
                        'size': size,
                        'used': used,
                        'available': available,
                        'percent_used': percent_used,
                        'mountpoint': mountpoint
                    })

                return filesystem_info
            else:
                return None
        except FileNotFoundError:
            print("O comando 'df' não está disponível no sistema.")
            return None

    def get_process_files_and_sizes(self, pid):
        command = ['lsof', '-Ftnsz', '-p', str(pid)]
        output = subprocess.check_output(command).decode('utf-8')
        lines = output.split('\n')[1:]
        files = {}
        current_file = None
        for line in lines:
            if line.startswith('n'):
                current_file = line[1:]
            elif line.startswith('s'):
                if current_file is not None:
                    file_size = int(line[1:])
                    files[current_file] = file_size
                    current_file = None
        return files                #Retorna um dicionário com a chave sendo o diretório do arquivo e o valor sendo o tamanho do arquivo

    