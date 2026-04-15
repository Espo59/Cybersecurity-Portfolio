# Python-Based Reverse Shell Simulation
This repository contains a Python-based implementation of a Reverse Shell (client-server architecture), developed for educational purposes 
to demonstrate how remote command execution and network socket communication function in a cybersecurity context.

---

# 🔍 Overview
A Reverse Shell is a technique where the target machine initiates a connection back to the attacker's listener server. 
This approach is often more effective than a bind shell because it can bypass most inbound firewall rules and Network Address Translation (NAT)
configurations, as the traffic appears to the firewall as an outbound connection.

---

# 🛠 Features
- **Reliable Data Framing:** Implements a custom protocol using a 4-byte length prefix (big-endian) to ensure complete message reconstruction and prevent
- data fragmentation over TCP.

- **Persistent Connection:** The client features an automatic reconnection mechanism with exponential backoff, ensuring the shell attempts to restore
the link if the server goes offline.

- **Multi-threaded Listener:** The server uses the threading library to handle multiple incoming connections simultaneously without blocking the main interface.

- **Integrated Directory Navigation:** Unlike standard subprocess calls, this implementation handles the cd command internally to maintain the state of the current working directory.

- **Dynamic Configuration:** Both scripts prompt the user for IP addresses and ports at runtime, allowing for flexible deployment in different lab environments.

---

# 🚀 Lab Setup & Usage

**Prerequisites**
Operating System: Linux, Windows, or macOS (Python 3.x installed).

Network: Both machines must be able to reach each other over the network.

Libraries: Standard library only (no external pip installations required).

**Execution**
Start the Listener (Server): Run this on the "Attacker" machine first:

Bash python3 reverse_shell_server.py

Enter the IP address to bind to (e.g., 0.0.0.0 for all interfaces).

The server will wait on port 8000 by default.

**Start the Client (Target)** 

Run this on the "Victim" machine:

Bash python3 reverse_shell_client.py

Enter the Server's IP address and the port (8000).

**Command Execution**
Once the prompt [IP address]$ appears on the server, type any system command (e.g., ls, whoami, ipconfig) to see the output from the remote machine.
Type exit to close the session.

---

# 🧠 Educational Objectives
This experiment was conducted to understand:

- Socket Programming: How TCP/IP connections are established, maintained, and closed using the socket library.

- Data Serialization: The use of the struct module to pack and unpack binary data for network transmission.

- Process Management: How the subprocess module interacts with the OS shell to execute commands and capture output.

- Defensive Security: Understanding why EDR (Endpoint Detection and Response) systems flag unencrypted reverse shells and the importance of monitoring outbound traffic.

---

# ⚠️ Disclaimer
FOR EDUCATIONAL PURPOSES ONLY. This tool is intended for use in controlled, private laboratory environments for cybersecurity research and learning. Unauthorized use of this script on networks you do not own or have explicit permission to test is illegal. As a cybersecurity student, I advocate for ethical hacking and responsible disclosure.
