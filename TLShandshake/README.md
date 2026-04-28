# 🔒 Python mTLS Secure Socket Communication Lab

This project implements a secure **Client-Server architecture using Mutual TLS (mTLS)** in Python.

Unlike standard TLS connections, **mTLS requires both client and server authentication**, ensuring a higher level of trust and security between communicating parties.

---

## 📌 Overview

This system demonstrates a full **Public Key Infrastructure (PKI)-based secure communication model**, where both endpoints verify each other using digital certificates.

Key concept:

* Server verifies client identity
* Client verifies server identity
* Communication is encrypted end-to-end

---

## 📂 Project Structure

### 🏗️ `server_client_cert_gen.py`

* Acts as a lightweight **Certificate Authority (CA)**
* Generates cryptographic key pairs
* Issues and signs X.509 certificates
* Manages PKI lifecycle for both client and server

---

### 🖥️ `secure_socket_server.py`

* TLS-enabled TCP server
* Enforces mandatory client certificate authentication
* Rejects unauthorized or unsigned connections
* Establishes encrypted communication channel

---

### 💻 `secure_socket_client.py`

* TLS client implementation
* Presents its own identity certificate
* Connects securely to the server
* Exchanges encrypted messages

---

## 🚀 Getting Started

---

### 📦 1. Prerequisites

Install required dependency:

```bash id="k7m3vp"
pip install cryptography
```

---

### 🔑 2. Generate Certificates (PKI Setup)

Before starting the system, generate the certificate infrastructure:

```bash id="x4n8ql"
python3 server_client_cert_gen.py gen_certs
```

This will create:

* `ca_cert.pem` / `ca_key.pem` → Root Certificate Authority
* `server_cert.pem` / `server_key.pem` → Server identity
* `client_cert.pem` / `client_key.pem` → Client identity

---

### 🖥️ 3. Start Secure Server

Run on the server machine:

```bash id="m9c3vz"
python3 secure_socket_server.py
```

* Listens on port **4433**
* Enforces certificate validation

---

### 💻 4. Start Secure Client

Run on the client machine:

```bash id="r7n2ql"
python3 secure_socket_client.py --host 127.0.0.1
```

Replace `127.0.0.1` with server IP if needed.

---

## 🔒 Security Features

### 🧾 Mutual Authentication (mTLS)

* Both client and server must present valid certificates
* Certificates must be signed by the trusted CA

---

### 🔐 Encrypted Communication

* TLS 1.2+ secure channel
* Prevents eavesdropping and data tampering

---

### 🛡️ Man-in-the-Middle Protection

* Certificate chain validation
* Rejects untrusted or self-signed peers

---

### 🧠 Identity-Based Trust Model

* Each endpoint has a cryptographic identity
* Trust is explicitly defined, not implicit

---

## 📖 Learning Objectives

This project demonstrates:

* Public Key Infrastructure (PKI) design
* X.509 certificate lifecycle management
* Mutual TLS authentication flow
* Secure socket programming in Python
* Secure client-server architecture design
* Real-world enterprise security communication patterns

---

## ⚠️ Security Considerations

### ❗ Important Notes

* Private keys must never be shared or uploaded to public repositories
* Use `.gitignore` to exclude sensitive files

Example:

```text id="t9m4vp"
*.key.pem
```

* This setup is intended for **lab and educational environments only**
* Production systems should use trusted external Certificate Authorities

---

## 🧪 Recommended Use Case

This project is ideal for:

* Cybersecurity learning environments
* PKI and TLS experimentation
* SOC analyst training labs
* Secure systems architecture studies

---

## 📄 License

This project is released under the MIT License.
