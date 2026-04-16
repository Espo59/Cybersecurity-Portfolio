# 🔗 P2P Remote Management & Command Execution Toolkit
This project consists of a decentralized Peer-to-Peer (P2P) infrastructure designed to explore network communication, remote command execution, 
and file synchronization between modern Linux systems (Kali/Ubuntu) and legacy environments (Metasploitable 2).

---

# ⚠️ Educational Purpose & Legal Disclaimer
This toolkit is for purely educational and authorized security testing purposes only.
- **Ethical Use:** Never deploy these scripts on networks or devices without explicit written permission.
- **Security Risk:** The "Victim" node intentionally allows remote code execution.
Do not run it on public-facing servers or untrusted networks.

---

# 🏗️ Architecture Overview
The system is composed of two primary components:

P2P Controller (p2p_node.py): 
 
 - A modern Python 3.x implementation for Kali Linux/Ubuntu. It acts as both a chat node and a remote administrator, capable of broadcasting commands and
uploading scripts to multiple peers.

 - P2P Victim (p2p_victim.py): A legacy Python 2.7 implementation optimized for Metasploitable 2. It remains in a passive listening state, executing commands received from authorized controllers.

---

# 🚀 Getting Started
**Setup on Metasploitable 2 (Victim)**

- Since Metasploitable 2 uses an older environment, run the script using Python 2. This node will wait for an incoming connection from the Controller.

*Command:*

 `bash python p2p_victim.py 8082 (e.g., 8082)`

**Setup on Kali Linux / Lubuntu (Controller)**

- The controller requires Python 3.8+ and should be started on a listening port to allow other nodes to connect back if needed.

*Command:*

`bash sudo python3 p2p_node.py 8080 (for Kalilinux)`

`bash sudo python3 p2p_node.py 8081 (for Lubuntu)`

---

# 🕹️ Establishing the Connection

Once both nodes are running, you must link them. 

The Controller (Kali) must initiate the connection to the Victim (Metasploitable).

Inside the Kali terminal (where p2p_node.py is running), use the following command:

`bash: connect (victim-ip) (victim-port)`

`connect 192.168.1.15 8082 (exemple of Metasploite ip and port)`

Inside Lubuntu terminal, use the following command:

`bash: connect (Kali-ip) (Kali-port)`

---

# 📋 Available Controller Commands
Once connected, you can manage the victim(s) using the interactive CLI:
Command-Syntax

List- list

Execute - exec (all) 

Status - status (all)

Upload - send_script (all)

Broadcast - send (message)

Exit - exit

---

# 🧪 Technical Features
**Legacy Compatibility:** p2p_victim.py uses the commands module for full compatibility with Python 2.7 environments.

**Threaded Handling:** Every connection is managed in a separate thread, allowing the controller to manage multiple victims simultaneously.

**Binary Handling:** The controller can push binary data (scripts) to a /tmp/ directory on the remote target and automatically set execution permissions
(chmod +x).
**Robust Parsing:** Improved EXEC parsing to prevent crashes on malformed network packets.
