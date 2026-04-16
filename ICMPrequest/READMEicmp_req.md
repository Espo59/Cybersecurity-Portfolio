# ICMP IP Spoofing Tool (Scapy-based)
This repository contains a Python script designed to demonstrate IP Source Address Spoofing using the ICMP protocol. 
It was developed as a laboratory experiment to study network protocol vulnerabilities and packet crafting.

---

# 🔍 How It Works
Standard network applications rely on the OS kernel to fill in the Source IP address. 
This script bypasses the standard networking stack using Scapy to craft a "Raw Socket" packet where the source IP is manually defined.

**Layer 3 (IP):** The script injects a fake source IP (SRC_IP) into the IP header.

**Layer 4 (ICMP):** An Echo Request (Type 8) is constructed with a custom payload.

Transmission: The packet is injected directly into the network interface.

---

# 🧪 Educational Objectives
- **Packet Manipulation:** Learning how to stack network layers (Ethernet/IP/ICMP) manually.

- **Security Testing:** Verifying if the local network infrastructure (switches/routers) implements BCP 38 or uRPF (Unicast Reverse Path Forwarding) to detect and drop spoofed packets.

- **Traffic Analysis:** Observing the discrepancy between the physical sender and the logical sender in tools like Wireshark.

---

# 🛠 Prerequisites
OS: Kalilinux (requires root privileges to use raw sockets).

Dependencies: Scapy library (pip install scapy).

Network Setup: Best tested in a virtualized lab environment (e.g., GNS3, VMware, or VirtualBox).

---

# 🚀 Usage
Update the SRC_IP, DST_IP, and IFACE constants in the script.

Run the script with root privileges:

`bash sudo python3 ping_spoofed.py`

Note: In a successful spoofing scenario, you will typically see a timeout in the script. 

This is because the target sends the "Echo Reply" to the spoofed IP address, not back to your machine. 
To verify success, monitor the network from the spoofed host or use a network sniffer.

---

# ⚠️ Disclaimer
FOR EDUCATIONAL PURPOSES ONLY.
This tool is intended for use in authorized penetration testing and controlled laboratory environments. Unauthorized spoofing of IP addresses on public or private networks is illegal and unethical.
