# Light C2  -  Command & Control (C2)
A lightweight, multi-threaded Python-based Command & Control (C2) system designed for managing multiple client connections and remotely executing commands equipped with a web interface for controlling connected clients. 

### Features:
- **Client-Server Architecture**: Multi-threaded server to handle multiple client connections simultaneously.
- **Remote Command Execution**: Send commands to connected clients and receive real-time output.
- **Web Interface**: 
  - View connected clients and their IP addresses in a tabbed layout.
  - Send commands to individual clients and view their results.

### Installation:
1. Clone the repository:
    ```bash
    git clone https://github.com/bhanunamikaze/Light-C2.git
    cd Light-C2
    ```
2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the server with required IP and port arguments on Attacker Server:
    ```bash
    python server.py -ip <SERVER_IP> -p <PORT>
    ```
4. Start the client on the Victim:
    ```bash
    python client.py
    ```

### Usage:
1. Open the web interface at `http://0.0.0.0:5000` (by default) to manage connected clients.
2. Send commands to individual clients via the interface.



### License:
This project is licensed under the MIT License.

