#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import string

# 1. Extended Alphabet: Includes lowercase letters, digits, and common punctuation/spaces.
# Using string.ascii_lowercase + string.digits for efficiency.
EXTENDED_ALPHABET = string.ascii_lowercase + string.digits + " .,!?;:@"

def optimized_cipher(text, key, mode):
    """
    Optimized version:
    - Calculates the total shift only once (key * rounds).
    - Uses a dictionary for instant lookup (O(1)).
    """
    result = []
    n = len(EXTENDED_ALPHABET)
    
    # Normalize the key: if decrypting, the shift is negative
    shift = key % n
    if mode == "decrypt":
        shift = -shift

    # Create a mapping dictionary to speed up execution for long texts
    mapping = {char: i for i, char in enumerate(EXTENDED_ALPHABET)}

    for char in text:
        lower = char.lower()
        if lower in mapping:
            current_index = mapping[lower]
            # Calculate new index using modulo to handle wrap-around
            new_index = (current_index + shift) % n
            new_char = EXTENDED_ALPHABET[new_index]
            
            # Restore original casing (Uppercase vs Lowercase)
            result.append(new_char.upper() if char.isupper() else new_char)
        else:
            # Keep character as is if it's not in our defined alphabet
            result.append(char)

    return "".join(result)

def ask_input(prompt, data_type=int, condition=None, error_message="Invalid value."):
    """
    Handles user input with validation and error checking.
    """
    while True:
        try:
            value = data_type(input(prompt))
            if condition and not condition(value):
                raise ValueError
            return value
        except ValueError:
            print(error_message)

def main():
    print("=== Caesar Cipher Pro ===")

    while True:
        print("\n1. Manual | 2. File | 3. Exit")
        choice = input("→ ").strip()

        if choice == "3": 
            break
        
        text = ""
        if choice == "1":
            text = input("Enter text: ")
        elif choice == "2":
            path = input("File path: ")
            if not os.path.exists(path):
                print("Error: File not found.")
                continue
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        else: 
            continue

        # Get mode and validate input
        mode = input("Mode (encrypt/decrypt): ").lower()
        while mode not in ["encrypt", "decrypt"]:
            mode = input("Error. Type 'encrypt' or 'decrypt': ").lower()

        base_key = ask_input("Key (integer): ", int)
        rounds = ask_input("Rounds (>=1): ", int, lambda x: x >= 1)

        # LOGICAL IMPROVEMENT: 
        # Instead of a for-loop that slows down the PC, we calculate the final key.
        # Shifting by 3 for 10 rounds is equivalent to shifting by 30 once.
        total_key = base_key * rounds

        result = optimized_cipher(text, total_key, mode)

        print(f"\n--- Result ({mode}) ---\n{result}\n---")

        # Optional save to file
        if input("Save? (y/n): ").lower() == "y":
            filename = input("File name: ")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
            print("Saved.")

        if input("\nAnother operation? (y/n): ").lower() != "y":
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Graceful exit on CTRL+C
        sys.exit(0)
