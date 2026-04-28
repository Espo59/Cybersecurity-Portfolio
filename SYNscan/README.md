# 🧪 SYN Scanner – Automated Network Discovery Tool

A lightweight network reconnaissance tool built with **Scapy** that performs TCP **SYN (Half-Open) scanning** combined with automatic host discovery via ICMP.

This project is designed for educational purposes to demonstrate port scanning techniques and network response analysis.

---

## 🚀 Features

### 🌐 Host Discovery

* Uses ICMP Echo Requests to verify host availability before scanning
* Reduces unnecessary scanning of inactive targets

---

### 🔍 TCP SYN (Half-Open) Scan

* Sends TCP SYN packets without completing the handshake
* Analyzes responses to identify port states
* Minimizes footprint on target-side logs

---

### 📦 Batch Processing

* Scans ports in configurable batches (default: 100 ports)
* Improves performance and reduces network load

---

### 🧠 Multi-Pass Analysis

* Performs an initial scan to detect open ports
* Executes a secondary validation pass for confirmation

---

### 🎨 Structured Output

* Color-coded terminal output (OPEN / CLOSED / FILTERED)
* Clear visualization of scan results

---

## 🛠 Requirements

* Python 3.x
* Scapy

Install dependency:

```bash id="k8m3vp"
pip install scapy
```

> ⚠️ Root privileges are required due to raw socket operations.

---

## 💻 Usage

Run the scanner with administrative privileges:

```bash id="x4n7ql"
sudo python3 syn_scan.py <TARGET_IP> [options]
```

---

## ⚙️ Scan Modes

### 🔹 Quick Mode (default)

* Scans ports 1–1024

```bash id="q2m9vz"
sudo python3 syn_scan.py 192.168.1.10
```

---

### 🔹 Common Ports Mode

* Scans the most commonly used service ports

```bash id="m7c3xp"
sudo python3 syn_scan.py 192.168.1.10 --common
```

---

### 🔹 Full Scan Mode

* Scans the entire TCP port range (1–65535)

```bash id="r8n2ql"
sudo python3 syn_scan.py 192.168.1.10 --full
```

---

## 🔍 Scanning Logic

The tool implements a standard **SYN scan (stealth scan)** methodology:

* **SYN Sent** → initiates connection attempt
* **SYN-ACK Received** → port is OPEN
* **RST Received** → port is CLOSED
* **No Response / ICMP Block** → port is FILTERED

If a SYN-ACK is received, the scanner immediately sends a **RST packet** to avoid completing the TCP handshake.

---

## 🧪 Learning Objectives

This project demonstrates:

* TCP/IP handshake mechanics
* Stealth scanning techniques (SYN scan behavior)
* Host discovery using ICMP
* Packet crafting using Scapy
* Network service enumeration strategies
* Firewall behavior analysis (filtered vs closed ports)

---

## 🛡 Security & Ethical Notice

This tool is intended strictly for **educational and authorized testing environments**.

* Do not scan networks without explicit permission
* Unauthorized scanning may violate laws or policies
* Use only in isolated lab environments (VMs, test networks)

---

## 📄 License

This project is released under the MIT License.
