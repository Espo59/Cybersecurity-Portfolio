# SYN Scanner - Auto Discovery
A lightweight and powerful network scanner built with Scapy to perform TCP SYN (Half-Open) scans. 
This tool includes auto-discovery features via ICMP probing and supports multiple scanning modes to identify OPEN, CLOSED, or FILTERED ports.

---

# 🚀 Features
- **Host Discovery:** Verifies host reachability via ICMP echo requests before initiating the port scan.

- **SYN Scan (Half-Open):** Sends TCP SYN packets and analyzes responses (SYN-ACK/RST) without completing the three-way handshake, reducing the footprint on target application logs.

- **Batch Processing:** Scans ports in configurable batches (default: 100) to optimize network resource usage and performance.

- **Detailed Analysis:** Once open ports are identified, the tool performs a secondary detailed pass to confirm their status.

- **Color-coded Output:** Clear terminal output using ANSI colors to quickly distinguish between port states.

---

# 🛠 Requirements
The program requires Python 3 and the Scapy library.

Bash pip install scapy

Note: Since the script manipulates low-level packets (Raw Sockets), root or administrator privileges are required to run it.

---

# 💻 Usage
Clone the repository and run the script with sudo:

Bashsudo python3 syn_scan.py <TARGET_IP> [options]


**Available Options:**

- *quick:* Scans ports 1 through 1024 (Default mode).

- *common:* Scans the top 100 most common ports (e.g., 21, 22, 80, 443, 3306, etc.).

- *full:* Scans the entire port range (1-65535).

*Examples:*

Bash sudo python3 syn_scan.py 192.168.1.10

*Full scan of all 65k ports:*

sudo python3 syn_scan.py 192.168.1.10 --full

*Scan only the most common service ports:*

sudo python3 syn_scan.py 192.168.1.10 --common

---

# 🔍 Scanning Logic
The script follows the standard Stealth (SYN) Scan protocol:

SYN Sent: Sends a TCP packet with the S flag.

SYN-ACK Received (0x12): The port is OPEN. The scanner immediately sends a RST to close the connection before it's fully established.

RST-ACK Received (0x14): The port is CLOSED.

No Response / ICMP Unreachable: The port is likely FILTERED by a firewall.

---

# ⚠️ Disclaimer
This tool is developed strictly for educational purposes and Ethical Hacking. Performing scans against targets without explicit authorization is illegal. The author assumes no liability for any misuse of this software.
