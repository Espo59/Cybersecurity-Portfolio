# Basic Python Reverse Shell (Listener & Main)
This repository contains a foundational implementation of a Reverse Shell system. It demonstrates the core principles of network programming,
remote command execution, and process management using Python's standard libraries.

---

# 🔍 Overview
This project consists of two main components:

- **listener.py (Server/Attacker):** A script that sits in an "listening" state, waiting for a remote connection to manage.

- **main.py (Client/Target):** A script designed to be executed on a target machine, which initiates a connection back to the
listener and provides a remote command-line interface.

---

# 🛠 Features
- **TCP Socket Communication:** Uses the socket module to establish reliable, stream-oriented connections.

- **Dynamic Directory Tracking:** The client monitors current path changes using os.getcwd() and sends updates to the server to
maintain an accurate command prompt.

- **Integrated Shell Execution:** Utilizes subprocess.run to execute system-level commands and capture both standard output (stdout) and error messages (stderr).

- **Internal cd Handling:** Implements a custom handler for the cd command using os.chdir, ensuring that directory changes persist across different commands.

---

# 🚀 Lab Setup & Usage
- *Prerequisites*

Python 3.x installed on both machines.
The machines must be on the same network or have a reachable routing path.

- *Execution Steps*

Configure the Client:
Open main.py and set the SERVER_IP variable to the IP address of your listener machine.

- *Python*

SERVER_IP = '192.168.1.XX' # Replace with your IP
Start the Listener:
On the attacker machine, run:

Bash
python3 listener.py

The server will start listening on port 8080.

- *Start the Client:*

On the target machine, run:

Bash
python3 main.py

- *Interact:*

Once connected, you can type commands directly into the listener. Type exit to safely close the connection on both ends.

---

# 🧠 Educational Objectives
This project was developed to explore:

**Networking Fundamentals:** Understanding the handshake and data exchange in a TCP/IP connection.

**Standard I/O Redirection:** Learning how to capture and transmit the output of system processes over a network.

**Protocol Design:** Creating a simple communication flow where the server and client exchange formatted strings to synchronize the working directory.

---

# ⚠️ Disclaimer
FOR EDUCATIONAL PURPOSES ONLY. This tool is intended for use in controlled, private laboratory environments for cybersecurity research and learning. Unauthorized use of this script on networks you do not own or have explicit permission to test is illegal.
