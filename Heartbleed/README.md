# 💔 Heartbleed Vulnerability Simulation (CVE-2014-0160) – Python 3

A Python 3 implementation and educational reconstruction of the **Heartbleed vulnerability (CVE-2014-0160)**, based on original Python 2 exploit concepts and adapted for modern environments.

This project demonstrates how a TLS implementation flaw can lead to unintended memory disclosure.

---

## 🔍 Project Overview

The Heartbleed vulnerability affects certain versions of OpenSSL and allows a remote party to read portions of server memory beyond intended boundaries.

This project is designed to illustrate:

* How TLS heartbeat extensions operate
* How memory over-read vulnerabilities occur
* The impact of missing bounds validation in secure protocols
* The importance of secure cryptographic implementation practices

---

## 🚀 Features

* Python 3 compatible implementation
* Manual and semi-automated testing modes
* Continuous request simulation (for stability testing in lab environments)
* Basic filtering of leaked memory output for analysis purposes
* Designed for controlled cybersecurity labs (e.g., SEED Labs)

---

## 🧩 Project Versions

### 🧪 `heartv2.py` – Initial Implementation

* Establishes TLS handshake manually
* Sends a single crafted heartbeat request
* Outputs raw memory response (hex + ASCII representation)

---

### ⚙️ `heartv3.py` – Enhanced Testing Version

* Sends multiple heartbeat requests per execution cycle
* Improves probability of capturing meaningful memory data
* Adds simple keyword filtering for analysis (`e.g. "password"`)

---

### 🤖 `heartbleed3.py` – Automated Simulation Mode

* Continuous execution loop for repeated testing
* Automatic reconnection handling
* Structured extraction of readable memory fragments for analysis

---

## 🛠️ Technical Details

* Low-level socket communication
* Manual TLS packet construction
* Custom implementation of Heartbeat request structure
* Hex and ASCII parsing of server responses
* No dependency on high-level SSL abstractions

---

## ⚙️ Requirements

* Python 3.x
* Root/Sudo privileges (depending on network configuration)
* A vulnerable or intentionally misconfigured test environment

  * Example: SEED Labs VM

---

## 🚀 Usage

Replace `[TARGET_IP]` with your lab target.

### Run Initial Version

```bash id="k8q1mp"
sudo python3 heartv2.py [TARGET_IP]
```

---

### Run Enhanced Version

```bash id="r4t9vz"
sudo python3 heartv3.py [TARGET_IP]
```

---

### Run Automated Simulation

```bash id="x6n3cs"
sudo python3 heartbleed3.py [TARGET_IP]
```

---

## 📖 Educational Objectives

This project is intended to support learning in:

* TLS/SSL protocol internals
* Memory safety vulnerabilities
* Secure coding practices in cryptographic libraries
* Real-world impact of software implementation flaws
* Cybersecurity lab experimentation

---

## 🧪 Recommended Environment

This project should only be executed in controlled environments such as:

* SEED Labs
* Virtualized vulnerable systems
* Isolated cybersecurity training networks

---

## ⚠️ Security Disclaimer

This project is strictly for educational and research purposes.

* Do not use against systems without explicit authorization
* Unauthorized access to systems is illegal
* Always operate within controlled lab environments

---

## 📄 License

This project is released under the MIT License.
