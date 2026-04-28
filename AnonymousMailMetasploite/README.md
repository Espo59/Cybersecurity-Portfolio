# 📧 SMTP Automation Tool (Metasploitable Lab)

A lightweight Python utility designed for educational and security testing purposes.
This tool automates the process of sending emails via SMTP, specifically in vulnerable lab environments such as Metasploitable where authentication may be absent or misconfigured.

> ⚠️ This project is intended for use in controlled lab environments only.

---

## 📌 Overview

This tool allows users to interactively construct and send emails through a target SMTP server.

It is designed to demonstrate:

* How the SMTP protocol operates without authentication
* Email spoofing concepts in insecure environments
* Basic network communication using Python’s built-in libraries

---

## 🚀 Features

* Interactive CLI for email creation (sender, recipient, subject, body)
* Support for MIME formatting using `MIMEMultipart`
* Multi-line message input with EOF termination
* Basic error handling for connection issues and timeouts

---

## 🛠️ Requirements

* Python 3.x
* A lab environment with an SMTP service running (e.g., Metasploitable on port 25)

No external dependencies are required. The script uses only standard Python libraries:

* `smtplib`
* `email`

---

## ⚙️ Configuration

Before running the script, update the target IP address:

```python id="u3r7zn"
target_ip = "192.168.xxx.xxx"  # Replace with your target machine IP
```

---

## 📋 Usage

### 1. Run the Script

```bash id="m7c2yf"
python3 mail_meta.py
```

---

### 2. Follow the Interactive Prompts

* **From:** Sender email (e.g., `admin@internal.lab`)
* **To:** Recipient username (e.g., `root`, `sys`)
* **Subject:** Email subject
* **Message:**

Type your message body. To send:

* Linux / macOS → `Ctrl + D`
* Windows → `Ctrl + Z` + Enter

---

## 📖 How It Works

The script connects to the target SMTP service on port 25 and performs a standard SMTP transaction:

1. Establishes a connection to the server
2. Builds a MIME-compliant email message
3. Sends SMTP commands (`MAIL FROM`, `RCPT TO`, `DATA`)
4. Terminates the session using `QUIT`

---

## 🧪 Learning Objectives

This project helps reinforce:

* Understanding of SMTP protocol behavior
* Awareness of insecure mail server configurations
* Practical scripting for network interaction
* Basic concepts of email spoofing in lab environments

---

## 🛡️ Security Notice

This tool is intended strictly for educational and authorized testing purposes.

* Do not use on systems without explicit permission
* Do not attempt email spoofing outside controlled environments
* Misuse may violate laws and ethical guidelines

---

## 📈 Future Improvements

* Add authentication support (LOGIN / TLS)
* Implement logging of SMTP responses
* Add input validation and sanitization
* Extend to support attachments

---

## 📄 License

This project is released under the MIT License.


Packages the user input into a MIME-compliant string.

Issues the MAIL FROM, RCPT TO, and DATA commands via smtplib.

Closes the session with QUIT.
