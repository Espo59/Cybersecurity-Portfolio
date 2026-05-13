# 🔐 Caesar Cipher Pro

A high-performance Python implementation of the Caesar Cipher algorithm, optimized for large texts and multiple execution rounds.

This version extends the traditional cipher by supporting a wider character set and applying mathematical optimizations to improve efficiency.

---

## 🚀 Features

* **Optimized Performance**
  Reduces time complexity from **O(n × rounds)** to **O(n)** using mathematical key aggregation

* **Extended Alphabet Support**
  Handles:

  * Lowercase and uppercase letters (case preserved)
  * Digits
  * Common punctuation (`.,!?;:@`)
  * Spaces

* **Multiple Input Modes**

  * Manual text input
  * File-based processing (`.txt`)

* **Fast Character Mapping**
  Uses dictionary-based lookup (`O(1)`) for efficient character translation

* **Output Persistence**
  Option to save results directly to a file

---

## 🛠️ How It Works

### Optimization Strategy

Instead of applying the shift repeatedly for each round, the script calculates a single effective key:

[
\text{Total Key} = \text{Base Key} \times \text{Rounds}
]

This ensures consistent performance regardless of the number of rounds.

---

## 📋 Requirements

* Python 3.6+

No external libraries are required.

---

## 🚀 Usage

### Run the Script

```bash id="k3m8qn"
python3 caesar_cipher.py
```

---

### Interactive Menu

* **Option 1 – Manual Input**
  Enter text directly from the terminal

* **Option 2 – File Input**
  Provide the path to a `.txt` file

* **Option 3 – Exit**
  Safely terminate the program

---

## ⚙️ Configuration

| Setting    | Description                                                 |
| ---------- | ----------------------------------------------------------- |
| **Key**    | Number of positions to shift                                |
| **Rounds** | Number of times the shift is applied (optimized internally) |
| **Mode**   | Choose between encryption or decryption                     |

---

## 📖 Learning Objectives

This project demonstrates:

* Algorithm optimization techniques
* Time complexity reduction strategies
* Efficient data structures (dictionary lookups)
* File handling in Python
* Basic cryptography concepts

---

## ⚠️ Security Notice

This project is intended for educational purposes only.

The Caesar Cipher is a classical encryption method and is **not secure** against modern cryptographic attacks.
It should not be used to protect sensitive or real-world data.

---

## 📈 Future Improvements

* Add support for custom alphabets
* Implement frequency analysis tools (for cracking the cipher)
* Add GUI interface
* Extend to more advanced ciphers (Vigenère, AES demo)

---

## 📄 License

This project is released under the MIT License.
