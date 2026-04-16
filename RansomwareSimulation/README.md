# Remote Ransomware Simulation Lab (Educational PoC)
This repository contains a Proof of Concept (PoC) designed to demonstrate the technical mechanics of a remote encryption attack, 
commonly associated with ransomware. The project is strictly intended for educational purposes, helping students and cybersecurity 
enthusiasts understand Command & Control (C2) communication and symmetric file encryption.

---

# 🎓 Educational Objectives
The goal of this lab is to explore:

- **Command & Control (C2) Logic:** How an attacker sends remote instructions to a compromised node.

- **Symmetric Encryption:** Utilizing the Fernet (AES-based) implementation to secure or lock files.

- **Network Sockets:** Managing persistent connections and multi-threaded request handling in Python.

- **Post-Exploitation Artifacts:** The creation of "ransom notes" as a triggered event after encryption.

---

# 🛠️ Project Components

### 1. The Controller (controller.py)
This script acts as the Attacker's Terminal. It is responsible for:

Generating a unique session key for encryption.

Establishing a TCP connection to the target machine.

Providing an interactive menu to trigger encryption or decryption remotely.

### 2. The Victim Node (victim.py)
This script represents the Target System. It stays in listening mode and:

Accepts incoming connections from the Controller.

Uses multi-threading to handle commands without interrupting its main loop.

Recursively crawls through specified directories to encrypt or decrypt files.

Automatically generates or removes a HACKED.txt note.

---

# 🚀 Lab Setup & Execution

### *Prerequisites*

Python 3.x

cryptography library installed on both nodes:

`bash pip install cryptography`

- ### Step 1: Start the Victim Node

Run this on the "target" machine (e.g., a Lubuntu VM):

`bash python3 victim.py`

The node will start listening on port 8080.

- ### Step 2: Connect via Controller

Run this on the "attacker" machine (e.g., Kali Linux):

`bash python3 controller.py`

Enter the IP address of the Victim Node.

Choose Option 1 to encrypt a directory. You will need to provide the full path on the victim's machine.

Check the victim's folder: all files (except the note) will be encrypted, and HACKED.txt will appear.

Choose Option 2 to decrypt and restore the files.

---

# ⚠️ Legal & Ethical Disclaimer
This project is for academic and ethical hacking purposes ONLY. 
Unauthorized access to computer systems or the use of this code for malicious intent is illegal. The authors are not responsible for any misuse of this software.
Always conduct your tests in isolated, authorized lab environments like Metasploitable or dedicated Virtual Machines.
