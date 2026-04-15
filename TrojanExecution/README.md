# Multi-Threaded Remote Execution System (Educational Simulation)
This repository contains a Python-based client-server architecture designed to simulate a remote script execution environment.
The system allows a central server to distribute a shell script (command.sh) to multiple connecting clients (bots), which then execute the payload locally.

---

# 🛠 Components
- **trojan_execution_server.py:** A multi-threaded TCP server that listens for incoming connections and serves the payload script.

- **trojan_execution_client.py:** A client that connects to the server, downloads the script into a temporary file, executes it, and cleans up.

- **command.sh:** A sample Bash script that simulates a DoS (HTTP Flood) attack for educational purposes.

---

# 🚀 How It Works
- **The Server**
The server uses socketserver.ThreadingTCPServer to handle multiple clients simultaneously.

It listens on a specific port (default: 8000).

When a client connects, it checks for the existence of command.sh.

If found, it transmits the file content; otherwise, it sends a SCRIPT_NOT_FOUND error.

- **The Client**
The client acts as the execution agent.

It connects to the server's IP and port.

It receives the script and saves it as a temporary .sh file.

It grants execution permissions (chmod 755) to the file.

It runs the script using subprocess.run and deletes the file immediately after.

- **The Payload (command.sh)**
The provided sample script performs a simulated HTTP Flood attack using curl.

*Target:* A local Metasploitable instance (Mutillidae).

*Method:* Sends multiple backgrounded GET requests to stress the web server.

---

# 📋 Usage
*Prerequisites*
Python 3.x

Linux/Unix environment (for the client and .sh execution)

curl installed on the client machine

- **Step 1:** Start the Server
On the machine that will host the script:

Bash python3 trojan_execution_server.py

- **Step 2:** Configure the Payload

Ensure command.sh is in the same directory as the server. You can modify the TARGET, REQUESTS, and DELAY variables inside the script.

- **Step 3:** Run the Client

On the target machine (or separate terminal), provide the server's IP and port:

sudo python3 trojan_execution_client.py <server_ip> <port>

sudo python3 trojan_execution_client.py 127.0.0.1 8000

---

# ⚠️ Disclaimer
For Educational Purposes Only.
This project is intended to demonstrate the mechanics of remote execution and the impact of DoS attacks in a controlled, academic environment 
(e.g., against a Metasploitable VM).

# Never use these scripts on systems you do not own.

# Never use these scripts on public networks.

The authors are not responsible for any misuse or damage caused by this software.

---

# 📝 License
This project is provided "as-is" for learning and research. You are free to modify and adapt it for your own educational labs.
