# Python File Encryption Suite
A lightweight, secure file encryption and decryption utility based on the Fernet (symmetric encryption) standard. This suite allows you to generate a secure key, encrypt all files within a target directory, and safely restore them.

---

# 🛠 Features
- **Symmetric Encryption:** Uses the cryptography library's Fernet implementation (AES-128 in CBC mode with HMAC authentication).

- **Batch Processing:** Automatically scans a specified directory to encrypt or decrypt all files at once.

- **Security:** Ensures that encrypted data cannot be read or modified without the specific 32-byte base64-encoded key.

---

# 📂 File Structure
*gen_key.py:*

- Generates a unique, secure binary key.

*encrypt.py:*

- Uses the key to transform plaintext files into ciphertext.

*decript.py:*

- Reverts ciphertext files back to their original state using the same key.

---

# 🚀 Getting Started

*Prerequisites*

You must have the cryptography library installed:

Bash pip install cryptography

- Generate a Key

First, create your unique encryption key. This will generate a file named key.txt.

Bash python3 gen_key.py

*Warning: Never share your key.txt. If you lose this file, you lose access to your encrypted data forever.*

- Encrypt Files

Place the files you wish to protect in a folder named targets. Then run:

Bash python3 encrypt.py

The script will read key.txt and overwrite all files in the targets directory with encrypted versions.

- Decrypt Files

To restore your files to their original state:

Bash python3 decript.py

The script will use key.txt to verify and decrypt the files. If the key is incorrect or the files are corrupted, the process will fail to prevent data damage.

---

# ⚠️ Security Disclaimer
This project is for educational and personal use.

Key Loss: There is no "password recovery" mechanism. No key = No data.

Overwriting: The scripts overwrite the original files during the process. It is highly recommended to keep a backup of your data before encrypting.

---

# 📝 License
This project is open-source and available for research and development purposes.
