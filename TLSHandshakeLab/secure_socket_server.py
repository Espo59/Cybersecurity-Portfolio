#!/usr/bin/env python3
import socket
import ssl

# =============== CONFIGURATION ===============
# These filenames now match the output of server_client_cert_gen.py
SERVER_CERT = "server_cert.pem"
SERVER_KEY = "server_key.pem"
CLIENT_CA = "ca_cert.pem"      # The CA certificate used to verify the client
HOST = "0.0.0.0"               # Listen on all available interfaces
PORT = 4433                    # Port must match the client's destination port

def main():
    # 1. Setup SSL Context for Mutual Authentication (mTLS)
    # Purpose.CLIENT_AUTH means this context will be used for a server that verifies clients
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Require the client to present a valid certificate
    context.verify_mode = ssl.CERT_REQUIRED
    
    # Load the server's identity (certificate + private key)
    try:
        context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
        # Load the CA certificate to verify the client's certificate
        context.load_verify_locations(cafile=CLIENT_CA)
    except FileNotFoundError:
        print(f"Error: Certificate files not found. Run the generator script first.")
        return

    # Set minimum TLS version to 1.2 for modern security standards
    try:
        context.minimum_version = ssl.TLSVersion.TLSv1_2
    except AttributeError:
        # Fallback for older Python/OpenSSL versions
        pass

    # 2. Setup standard TCP Socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        # Allow immediate reuse of the port after stopping the server
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"[SERVER] Listening on {HOST}:{PORT}...")

        while True:
            # Accept the raw TCP connection
            newsock, addr = sock.accept()
            print(f"[SERVER] TCP connection accepted from {addr}")
            
            # 3. Wrap the socket with TLS
            # This triggers the SSL/TLS handshake
            try:
                with context.wrap_socket(newsock, server_side=True) as ssock:
                    print(f"[SERVER] TLS Handshake successful. Version: {ssock.version()}")

                    # Optional: Inspect the client's certificate details
                    try:
                        cert = ssock.getpeercert()
                        # Extract the Common Name (CN) from the subject
                        subject = dict(x[0] for x in cert['subject'])
                        client_cn = subject.get('commonName', 'Unknown')
                        print(f"[SERVER] Authenticated Client CN: {client_cn}")
                    except Exception:
                        print("[SERVER] Could not retrieve client certificate details.")

                    # 4. Data Exchange
                    try:
                        # Receive encrypted data (automatically decrypted by ssock)
                        data = ssock.recv(4096)
                        if not data:
                            print("[SERVER] Received 0 bytes - connection closed by client.")
                        else:
                            # Decode UTF-8 and handle potential errors
                            text = data.decode("utf-8", errors="replace").strip()
                            print(f"[SERVER] Received (Decrypted): {text}")
                            
                            # Send a response (Echo back in uppercase)
                            response = f"SERVER ECHO: {text.upper()}"
                            ssock.sendall(response.encode("utf-8"))
                            
                    except socket.timeout:
                        print("[SERVER] Connection timed out during receive.")
                    except Exception as e:
                        print(f"[SERVER] Error during data exchange: {e}")
                        
            except ssl.SSLError as e:
                print(f"[SERVER] SSL Error (Handshake failed): {e}")
            except Exception as e:
                print(f"[SERVER] Generic connection error: {e}")

if __name__ == "__main__":
    main()
