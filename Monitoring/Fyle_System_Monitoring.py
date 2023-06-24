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

    