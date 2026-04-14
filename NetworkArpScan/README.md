# Network Discovery & ARP Scanner (Scapy-based)
This Python script is a high-performance network reconnaissance tool designed to discover active hosts within a Local Area Network (LAN). It utilizes the Address Resolution Protocol (ARP) to map IP addresses to their respective hardware (MAC) addresses.

---

# 🔍 How It Works
Unlike standard scanners that rely on ICMP (Ping), which is often blocked by modern firewalls and host-based security software, this tool operates at Layer 2 (Data Link Layer).

- **Frame Construction:** The script crafts a custom Ethernet frame with a broadcast destination address (ff:ff:ff:ff:ff:ff).

- **ARP Encapsulation:** It embeds an ARP "who-has" request (Opcode 1) inside the Ethernet frame for every IP in the target range.

- **Broadcast Emission:** The frames are sent across the network segment.

- **Response Parsing:** It captures ARP "is-at" replies (Opcode 2). Since ARP is essential for local communication, active hosts will respond with their MAC address even if they are configured to ignore pings.

---

# 🛠 Features
**CIDR Support:** Scan entire subnets (e.g., 192.168.1.0/24) or specific IP ranges.

**Interface Selection:** Choose the specific network interface (eth0, wlan0, etc.) for the scan.

**Custom Timeouts:** Adjustable wait times for responses to balance speed and accuracy.

**Dynamic Interface Validation:** Automatically checks if the specified network interface exists on the host system.

**Formatted Output:** Clear mapping of IP Address -> MAC Address.

---

# 🧪 Educational Objectives
This project was developed to explore:

The mechanics of Layer 2 broadcasting.

The role of the ARP Cache in local network routing.

Using Scapy for advanced packet manipulation and raw socket communication.

---

# 🚀 Usage
**Prerequisites**
Linux OS (Kali Linux, Parrot, or Ubuntu recommended).

Python 3.x and Scapy library.

Root Privileges (Required for crafting raw Layer 2 frames).

**Installation**
Bash
pip install scapy

**Execution**
Bash
sudo python3 arp_sweep.py -n 192.168.1.0/24 -i eth0

---

# ⚠️ Disclaimer
FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY.
This tool is intended for use in controlled laboratory environments. Unauthorized scanning of networks is unethical and may be illegal. Always obtain explicit permission before performing any security assessment.
