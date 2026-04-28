# 📦 Scapy IP Packet Inspector

A lightweight Python utility designed to demonstrate the internal structure of an **Internet Protocol (IP) packet** using the Scapy library.

This tool is strictly analytical and does not transmit any network traffic.

---

## 🔍 How It Works

Scapy represents network protocols as Python objects, allowing direct inspection and manipulation of packet headers that are normally managed by the operating system’s TCP/IP stack.

### 🧱 Packet Construction

* The script initializes an `IP()` object representing a Layer 3 IPv4 packet
* The `dst` (destination) field is explicitly set by the user
* All other fields (TTL, ID, flags, checksum, etc.) remain in their default state

---

### 🔎 Introspection Process

The tool uses Scapy’s built-in inspection capabilities:

* `ls()` → Displays all available fields of the IP layer
* `summary()` → Provides a human-readable representation of the packet
* Object introspection → Reveals internal structure of the IPv4 header

---

## 🛠 Features

* **Zero Network Transmission**
  Fully safe: no packets are sent or received

* **IPv4 Header Inspection**
  Displays all 14 standard fields of an IP header, including:

  * Version
  * IHL (Header Length)
  * Type of Service (TOS)
  * Total Length
  * Identification
  * Flags
  * TTL
  * Protocol
  * Checksum
  * Source / Destination IP

* **Field-Level Access**
  Demonstrates how individual packet attributes can be accessed programmatically

* **Lightweight Design**
  Minimal implementation focused purely on educational clarity

---

## 🧪 Educational Objectives

This project helps understand:

* Structure of the IPv4 header (RFC 791)
* How Scapy abstracts network protocols into Python objects
* Difference between default vs. customized packet fields
* Basic techniques for debugging network scripts
* Relationship between raw packet structures and OS-level networking

---

## 🚀 Requirements

* Python 3.x
* Scapy

Install dependency:

```bash id="t4k8vp"
pip install scapy
```

---

## ▶️ Usage

No root privileges are required since the script does not interact with the network stack.

```bash id="q2m7xn"
python3 ip_inspector.py
```

---

## 📋 Example Output

The script displays a structured breakdown of the IP layer, including:

* `version` → IPv4 version
* `ihl` → Header length
* `ttl` → Time To Live
* `proto` → Encapsulated protocol
* `dst` → Destination IP address

---

## 📖 Learning Objectives

This tool is intended for foundational understanding of:

* IPv4 packet structure
* Scapy object model
* Network protocol abstraction
* Packet inspection and debugging techniques
* OSI Layer 3 fundamentals

---

## ⚠️ Disclaimer

This project is intended for educational purposes only.

It is designed to help students and researchers understand packet structures and should not be used for any malicious or unauthorized network activity.

---

## 📄 License

This project is released under the MIT License.

