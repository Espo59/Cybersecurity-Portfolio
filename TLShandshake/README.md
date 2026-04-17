# Python mTLS Secure Socket Communication

This project provides a robust implementation of a secure Client-Server architecture using **Mutual TLS (mTLS)** in Python. Unlike standard HTTPS where only the server is verified, mTLS requires both the client and the server to authenticate each other using digital certificates.

---

# 📂 Project Structure

* `server_client_cert_gen.py`: A utility tool to manage the PKI (Public Key Infrastructure). It acts as a Certificate Authority (CA) to generate, sign, and issue certificates for both the server and the client.
* `secure_socket_server.py`: A secure TCP server that enforces mandatory client authentication.
* `secure_socket_client.py`: An interactive TCP client that connects to the server using its own identity certificate.

----

# 🚀 Getting Started

### 1. Prerequisites
Ensure you have the `cryptography` library installed (required by the generator script):

`bash pip install cryptography`

### 2. Generate Certificates
Before running the server or client, you must create the security credentials. Run the generator script:

`bash python3 server_client_cert_gen.py gen_certs`

This will generate the following files in your directory:

- *ca_cert.pem / ca_key.pem:* The Root Authority.

- *server_cert.pem / server_key.pem:* Identity for the Server.

- *client_cert.pem / client_key.pem:* Identity for the Client.

### 3. Run the Server

Start the server first. It will wait for incoming secure connections on port 4433.

`bash python3 secure_socket_server.py`

### 4. Run the Client

In a new terminal, start the client. You can specify the server IP (default is 127.0.0.1).

`bash python3 secure_socket_client.py --host 127.0.0.1`

---

# 🔒 Security Features

### Mutual Authentication: The connection fails if the client does not provide a certificate signed by the trusted CA.

### Encrypted Traffic: All data exchanged is encrypted using TLS 1.2+.

### Integrity: Prevents Man-in-the-Middle (MITM) attacks by verifying the Certificate Authority chain.

---

# ⚠️ Important Note

This repository includes a certificate generation script for educational and testing purposes. In a production environment:

Never upload private keys (.key.pem) to public repositories.

Use a .gitignore file to exclude sensitive files:

*Plaintext*

* *.key.pem*

*Use certificates issued by a recognized Public CA for production systems.*

---

# 📜License
This project is open-source and available under the MIT License.
