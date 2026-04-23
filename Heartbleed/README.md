# Heartbleed Exploit (CVE-2014-0160) – Python 3

A modern Python 3 implementation of the Heartbleed exploit, reconstructed from original Python 2 code and progressively enhanced into a fully automated tool.

---

# 🔍 Project Overview

The Heartbleed vulnerability allows an attacker to read the memory of a vulnerable server,
potentially exposing sensitive data such as session cookies, usernames, and passwords.

This project demonstrates:

* How the exploit works at protocol level
*  How memory over-read vulnerabilities leak sensitive data
*  Why secure input validation is critical in cryptographic software

---

# 🚀 Features

Fully compatible with Python 3

Manual and automated exploit modes

Continuous attack loop with auto-reconnect

Keyword-based memory filtering ("password")

Clean extraction of sensitive data from memory leaks

Designed for lab environments (e.g., SEED Labs)

---

# 🧩 Versions
## 🧪 heartv2.py — Initial Port
First stable Python 3 version

*Implements:*

TLS Client Hello handshake

Single Heartbeat request

Outputs raw leaked memory (hex + ASCII)

## ⚙️ heartv3.py — Improved & Filtered
*Implements:*

Adds burst mode (5 heartbeats per run)

Increases probability of capturing useful memory

 Filters output when "password" is detected
 
## 🤖 heartbleed3.py — Final Version
*Implements:*

Fully automated exploit

Continuous loop (while True)

Automatic reconnection if target resets connection

Extracts readable credential fragments from leaked memory

---

# 🛠️ Technical Details

* Low-level socket communication
* Manual crafting of TLS packets
* Custom Heartbeat request implementation
* Hex/ASCII parsing of leaked memory
* No reliance on high-level SSL libraries

---

# ⚙️ Prerequisites
Python 3.x

Root/Sudo privileges (may be required depending on environment)

A vulnerable target (e.g., SEED Labs Ubuntu 12 VM)

Usage

Replace [TARGET_IP] with your target system.

## *Run Version 2:*

`sudo python3 heartv2.py [TARGET_IP]`

## *Run Version 3:*

`sudo python3 heartv3.py [TARGET_IP]`

## *Run Final Version (Automated):*

`sudo python3 heartbleed3.py [TARGET_IP]`

---

# 📚 Educational Purpose

This project is intended for:

Cybersecurity students 👨‍💻👩‍💻

Ethical hacking labs 🧪

Understanding real-world vulnerabilities 🔍

It is particularly suited for environments like SEED Labs.

---

# ⚠️ Disclaimer

This project is for educational and research purposes only. Do NOT use these tools on systems without explicit authorization. 
Unauthorized access to computer systems is illegal and may result in criminal charges.
