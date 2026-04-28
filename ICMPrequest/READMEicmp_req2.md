# 🧠 ICMP Forensic & Protocol Analysis Tool

This Python script is a network analysis tool designed to perform **deep packet inspection (DPI)** on ICMP traffic.

It is intended for cybersecurity education and helps visualize how IPv4 and ICMP packets are structured at a low level.

---

## 🛠 Features

### 📦 Raw Packet Crafting

Uses **Scapy** to bypass the operating system network stack and construct custom IP/ICMP packets.

---

### 🔍 Forensic Packet Breakdown

Instead of simply reporting a ping response, the tool performs a full inspection of the packet:

#### 🌐 IP Layer Analysis

* IP Version
* IHL (Internet Header Length)
* TOS / DSCP values
* Fragmentation flags (DF / MF)
* TTL (Time To Live)
* Header checksum

#### 📡 ICMP Layer Analysis

* Type (Echo Request / Reply)
* Code
* Identifier (ID)
* Sequence number

#### 📦 Payload Inspection

* Decodes packet payload
* Displays human-readable preview
* Provides hex sample for low-level inspection

#### 🧾 Hex Dump Output

* Full packet representation in hexadecimal
* Enables bit-level and protocol-level analysis

---

## 🧪 Cybersecurity Use Cases

* **Packet Structure Learning**
  Understand how ICMP and IPv4 headers are constructed

* **OS Fingerprinting Analysis**
  Observe differences in:

  * Default TTL values
  * IP ID generation patterns
  * Response behavior across operating systems

* **Network Security Testing**
  Evaluate firewall and IDS/IPS handling of ICMP traffic

* **Hex-Level Packet Analysis**
  Map raw binary data to human-readable protocol fields

---

## 🚀 Requirements

* Python 3.x
* Scapy

Install dependency:

```bash id="h3k8vn"
pip install scapy
```

---

## ⚙️ Configuration

Update the following variables inside the script:

* `SRC_IP` → Source IP address
* `DST_IP` → Destination IP address
* `IFACE` → Network interface

---

## ▶️ Usage

Run the script with root privileges:

```bash id="k9m2qx"
sudo python3 ping_spoofed_explain.py
```

---

## ⚠️ Important Behavior Note

When using a spoofed source IP:

* The script may show a **timeout response**
* This is expected behavior

### Why this happens

The ICMP reply is sent to the **spoofed IP address**, not the attacker machine.

### Verification

To confirm packet delivery:

* Use Wireshark or tcpdump
* Monitor traffic from the spoofed host or target network segment

---

## 📖 Learning Objectives

This project reinforces:

* Deep Packet Inspection (DPI) concepts
* Structure of IPv4 and ICMP protocols
* Network debugging and forensic analysis
* Relationship between raw packets and OSI layers
* Practical understanding of traffic flow in IP networks

---

## 📄 License

This project is released under the MIT License.
