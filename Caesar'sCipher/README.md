# Caesar Cipher Pro
A high-performance Python implementation of the Caesar Cipher algorithm, optimized for large texts and multiple execution rounds.
This tool supports an extended alphabet including digits, punctuation, and spaces, making it more versatile than traditional implementations.

---

# 🚀 Features
- **Optimized Performance:** Uses a mathematical shortcut to calculate total shifts, reducing time complexity from $O(n \times rounds)$ to $O(n)$.

- **Extended Alphabet:** Supports lowercase, uppercase (preserved), digits, and common punctuation
( .,!?;:@).Multiple Modes: Options for manual text input or direct file processing.

- **Dictionary Lookup:** Utilizes $O(1)$ dictionary mapping forcharacter translation, ensuring lightning-fast execution even on long documents.

- **Persistence:** Allows saving results directly to a text file.

---

# 🛠 How It Works

- *The Optimization Logic*

Unlike basic scripts that loop through the encryption process for every "round" requested, this version calculates the total key first:

$$\text{Total Key} = \text{Base Key} \times \text{Rounds}$$

This ensures that whether you run 1 round or 1,000,000 rounds, the processing time remains the same.

---

# 📋 UsagePrerequisites
Python 3.6+Running the ScriptClone the repository or download caesar_chiper.py.
Run the script in your terminal:

`python3 caesar_chiper.py`

**Interactive Menu**

- *Option 1 (Manual):* Type your message directly into the terminal.

- *Option 2 (File):* Provide the path to a .txt file to encrypt/decrypt its entire content.

- *Option 3 (Exit):* Close the program safely.

--- 

# ⚙️ Configuration
Setting - Description

Key - The integer number of positions to shift in the alphabet.

Rounds - How many times the shift should be applied (optimized mathematically).

Mode - Choose between encrypt to secure text or decrypt to revert it.

---

# ⚠️ Disclaimer
This project is for educational purposes only. While the Caesar Cipher is a great way to learn about cryptography and programming logic,
it is not secure against modern cryptanalysis and should not be used to protect sensitive or private data.
