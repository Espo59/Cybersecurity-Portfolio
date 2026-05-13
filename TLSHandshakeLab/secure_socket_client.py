#!/usr/bin/env python3
import argparse
import socket
import ssl
import sys

# =============== CONFIGURATION ===============
# Default values - adjusted to match server_client_cert_gen.py output
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4433
CLIENT_CERT = "client_cert.pem"
CLIENT_KEY = "client_key.pem"
SERVER_CA = "ca_cert.pem"  # The CA certificate to verify the server

def build_context(cafile: str, certfile: str, keyfile: str, check_hostname: bool) -> ssl.SSLContext:
    """
    Creates and configures the SSL context for Mutual Authentication (mTLS).
    """
    # Create context for client-side (Purpose.SERVER_AUTH)
    # This automatically sets up standard verification of the server
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    
    # Load the client's own certificate and private key for mTLS
    try:
        ctx.load_cert_chain(certfile=certfile, keyfile=keyfile)
    except FileNotFoundError:
        print(f"Error: Certificate or Key file not found ({certfile}/{keyfile})")
        sys.exit(1)

    # Require valid certificate from the server
    ctx.verify_mode = ssl.CERT_REQUIRED
    
    # Hostname verification: set to True if the certificate Common Name matches the IP/Domain
    # Set to False if using local IPs without proper SAN (Subject Alternative Name)
    ctx.check_hostname = check_hostname
    
    # Enforce modern TLS version
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    except AttributeError:
        pass
        
    return ctx

def main():
    # Command line argument parsing
    ap = argparse.ArgumentParser(description="mTLS Secure Socket Client")
    ap.add_argument("--host", default=DEFAULT_HOST, help="Server Hostname/IP")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server Port")
    ap.add_argument("--cafile", default=SERVER_CA, help="CA file to verify server")
    ap.add_argument("--cert", default=CLIENT_CERT, help="Client certificate file")
    ap.add_argument("--key", default=CLIENT_KEY, help="Client private key file")
    ap.add_argument("--check-hostname", action="store_true", help="Enable SSL hostname verification")
    ap.add_argument("--io-timeout", type=float, default=10.0, help="Socket timeout in seconds")
    
    args = ap.parse_args()

    # 1. Build the Secure Context
    context = build_context(args.cafile, args.cert, args.key, args.check_hostname)

    print(f"[client] Connecting to {args.host}:{args.port}...")

    try:
        # 2. Create a standard TCP connection
        with socket.create_connection((args.host, args.port), timeout=args.io_timeout) as sock:
            
            # 3. Wrap the socket with SSL/TLS
            # server_hostname is needed for SNI and hostname verification
            with context.wrap_socket(sock, server_hostname=args.host) as ssock:
                print(f"[client] TLS Connection established. Version: {ssock.version()}")
                
                # Verify server identity
                server_cert = ssock.getpeercert()
                subject = dict(x[0] for x in server_cert['subject'])
                print(f"[client] Connected to Server CN: {subject.get('commonName', 'Unknown')}")

                # 4. Interactive loop
                print("Type your message (or press Ctrl+C to exit):")
                while True:
                    try:
                        message = input("> ")
                    except EOFError:
                        break
                        
                    if not message:
                        print("[client] Empty message: closing session.")
                        break

                    # Send the message (UTF-8 encoded)
                    ssock.sendall((message + "\n").encode("utf-8"))

                    # 5. Receive Response
                    try:
                        data = ssock.recv(4096)
                        if not data:
                            print("[client] Server closed the connection.")
                            break
                        
                        decoded_response = data.decode("utf-8", errors="replace").rstrip("\n")
                        print(f"[client] Response (Decrypted): {decoded_response}")
                        
                    except socket.timeout:
                        print(f"[client] Timeout: no response within {args.io_timeout}s")

                # Graceful shutdown
                try:
                    ssock.shutdown(socket.SHUT_WR)
                except OSError:
                    pass

    # Error Handling
    except ssl.SSLError as e:
        print(f"[client] SSL Error: {e}")
        sys.exit(1)
    except socket.timeout:
        print("[client] Connection timed out.")
        sys.exit(1)
    except ConnectionRefusedError:
        print("[client] Connection refused. Is the server running?")
        sys.exit(1)
    except Exception as e:
        print(f"[client] Generic Error: {type(e).__name__} - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
