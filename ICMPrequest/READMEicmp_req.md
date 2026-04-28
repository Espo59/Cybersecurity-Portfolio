# 🌐 ICMP IP Spoofing Tool (Scapy-based)

This repository contains a Python script that demonstrates **IP source address spoofing** using the ICMP protocol.

It is designed as a controlled laboratory experiment to study network packet crafting and protocol-level vulnerabilities.

---

## 🔍 How It Works

This tool bypasses the operating system’s networking stack by using **Scapy** to construct raw packets with custom parameters.

### Packet Structure

* **Layer 3 (IP)**

  * Manually sets a forged source IP address (`SRC_IP`)

* **Layer 4 (ICMP)**

  * Builds an ICMP Echo Request (Type 8) with a custom payload

* **Transmission**

  * Sends the crafted packet directly through the selected network interface

---

## 🧪 Educational Objectives

This project helps to understand:

* **Packet crafting fundamentals**

  * Manual construction of IP and ICMP layers using Scapy

* **Network security mechanisms**

  * Testing defenses such as BCP 38 and uRPF (anti-spoofing protections)

* **Traffic analysis techniques**

  * Observing differences between logical and physical packet origins using tools like Wireshark

---

## 🛠️ Requirements

* **Operating System:** Linux (Kali Linux recommended)
* **Privileges:** Root access required (raw sockets)
* **Dependencies:** Scapy

Install Scapy:

```bash id="p7x2kt"
pip install scapy
```

* **Recommended environment:** Virtual lab (VirtualBox, VMware, GNS3)

---

## 🚀 Usage

### 1. Configure the Script

Update the following variables inside the script:

* `SRC_IP` → Spoofed source IP address
* `DST_IP` → Target destination IP
* `IFACE` → Network interface

---

### 2. Run the Tool

```bash id="c4m9vz"
sudo python3 ping_spoofed.py
```

---

## 📊 Expected Behavior

In a successful spoofing scenario:

* The script may show a **timeout response**
* This is expected behavior

### Why?

The target system sends the ICMP Echo Reply to the **spoofed IP address**, not back to the attacker machine.

### Verification Methods

* Network sniffing (Wireshark)
* Monitoring traffic on the spoofed host

---

## 📖 Learning Outcomes

This project demonstrates:

* Low-level packet injection using Scapy
* IP header manipulation
* Network-layer trust assumptions
* Basic anti-spoofing mechanisms in modern networks
* Real-world packet flow analysis

---

## ⚠️ Security Disclaimer

This tool is intended strictly for educational and authorized testing purposes.

* Do not use on networks without explicit permission
* IP spoofing on unauthorized systems is illegal
* Always operate in controlled lab environments

---

## 📄 License

This project is released under the MIT License.
