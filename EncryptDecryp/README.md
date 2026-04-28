# 🔐 Python File Encryption Suite

A lightweight file encryption and decryption utility built using the **Fernet symmetric encryption standard** from the `cryptography` library.

This tool allows secure generation of encryption keys, batch file encryption, and safe restoration of encrypted data.

---

## 🛠 Features

* **Symmetric Encryption (Fernet / AES-based)**
  Uses authenticated encryption (AES + HMAC) ensuring confidentiality and integrity

* **Batch File Processing**
  Automatically encrypts or decrypts all files inside a target directory

* **Strong Key Security**
  Uses a 32-byte base64-encoded key for encryption and decryption

* **Simple Workflow**
  Split into modular scripts for key generation, encryption, and decryption

---

## 📂 Project Structure

* `gen_key.py`
  → Generates a secure encryption key (`key.txt`)

* `encrypt.py`
  → Encrypts all files inside the `targets/` directory

* `decript.py`
  → Decrypts files back to their original state using the same key

---

## 🚀 Getting Started

### Prerequisites

Install the required dependency:

```bash id="v4k2xm"
pip install cryptography
```

---

### 🔑 Step 1 – Generate Encryption Key

```bash id="c8r3jp"
python3 gen_key.py
```

This will create a `key.txt` file containing your encryption key.

> ⚠️ Important: If you lose this key, encrypted data cannot be recovered.

---

### 🔒 Step 2 – Encrypt Files

1. Place files inside the `targets/` directory
2. Run the encryption script:

```bash id="m2p7ql"
python3 encrypt.py
```

All files in the directory will be encrypted using the generated key.

---

### 🔓 Step 3 – Decrypt Files

```bash id="x9n4sv"
python3 decript.py
```

This will restore all encrypted files to their original state using `key.txt`.

---

## 📖 How It Works

This tool uses **Fernet symmetric encryption**, which provides:

* AES encryption for confidentiality
* HMAC authentication for integrity
* Protection against tampering and unauthorized modifications

Each file is processed in batch mode and securely transformed using the same key.

---

## ⚠️ Security Disclaimer

This project is intended for educational and personal use only.

* 🔑 **Key Loss** → If `key.txt` is lost, data cannot be recovered
* ⚠️ **File Overwrite** → Original files may be overwritten during processing
* 💾 **Backup Recommended** → Always backup important data before encryption

---

## 🧪 Learning Objectives

This project demonstrates:

* Practical implementation of symmetric cryptography
* Secure key management concepts
* File system automation in Python
* Batch processing techniques
* Real-world encryption workflow structure

---

## 📈 Future Improvements

* Add password-based key derivation (PBKDF2 / Argon2)
* Implement file integrity verification system
* Add GUI for non-technical users
* Support selective file encryption
* Improve logging and audit trail

---

## 📄 License

This project is open-source and intended for educational and research purposes.
