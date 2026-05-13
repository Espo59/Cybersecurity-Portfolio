#!/usr/bin/env python3
"""
Full implementation of an SSL Server and Client with Mutual Authentication (mTLS).
Includes automatic certificate generation and robust error handling.

Instructions:
1. Copy this code to both the server and client machines.
2. Generate certificates on the server: python3 server_client_cert_gen.py gen_certs
3. Copy the following files to the client: ca_cert.pem, client_cert.pem, and client_key.pem
4. Start the server: python3 server_client_cert_gen.py server <server_ip>
5. Start the client: python3 server_client_cert_gen.py client <server_ip>
"""

import socket
import ssl
import os
import sys
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# =============== CONFIGURATION ===============
PORT = 4433                      # Server listening port
BUFFER_SIZE = 1024               # Communication buffer size
BACKLOG = 5                      # Maximum number of queued connections

# Certificate filenames
CA_CERT_FILE = 'ca_cert.pem'          # CA Certificate
CA_KEY_FILE = 'ca_key.pem'            # CA Private Key
SERVER_CERT_FILE = 'server_cert.pem'  # Server Certificate
SERVER_KEY_FILE = 'server_key.pem'    # Server Private Key
CLIENT_CERT_FILE = 'client_cert.pem'  # Client Certificate
CLIENT_KEY_FILE = 'client_key.pem'    # Client Private Key

# Certificate Authority Information
CA_INFO = {
    "country": "IT",
    "state": "Italy",
    "locality": "Rome",
    "organization": "My CA",
    "common_name": "myca.example.com",
    "valid_days": 3650  # 10 years
}

# Server Certificate Information
SERVER_INFO = {
    "country": "IT",
    "state": "Italy",
    "locality": "Milan",
    "organization": "Server Org",
    "common_name": "server.example.com",  # Must match the hostname/IP
    "valid_days": 365  # 1 year
}

# Client Certificate Information
CLIENT_INFO = {
    "country": "IT",
    "state": "Italy",
    "locality": "Turin",
    "organization": "Client Device",
    "common_name": "client.example.com",
    "valid_days": 365  # 1 year
}

# =============== CERTIFICATE GENERATION FUNCTIONS ===============

def generate_private_key(key_file: str, key_size: int = 2048) -> rsa.RSAPrivateKey:
    """
    Generates an RSA private key and saves it to a PEM file.
    """
    # Generate RSA key with public exponent 65537
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    
    # Write to file in PEM format without encryption (NoPassword)
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    return private_key

def generate_ca_certificate() -> tuple:
    """
    Generates a self-signed certificate for the Certificate Authority (CA).
    """
    print("Generating CA certificate...")
    
    # 1. Generate CA private key
    ca_key = generate_private_key(CA_KEY_FILE)
    
    # 2. Define subject and issuer (identical for self-signed)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, CA_INFO["country"]),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, CA_INFO["state"]),
        x509.NameAttribute(NameOID.LOCALITY_NAME, CA_INFO["locality"]),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, CA_INFO["organization"]),
        x509.NameAttribute(NameOID.COMMON_NAME, CA_INFO["common_name"]),
    ])
    
    # 3. Build the certificate with CA-specific extensions
    cert = (x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=CA_INFO["valid_days"]))
        # Critical CA extensions
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        # Key Identifiers
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
        # Key Usage for CA
        .add_extension(x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,    # Can sign certificates
            crl_sign=True,         # Can sign CRLs
            encipher_only=False,
            decipher_only=False),
            critical=True)
        .sign(ca_key, hashes.SHA256(), default_backend()))
    
    # 4. Save to file
    with open(CA_CERT_FILE, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    return ca_key, cert

def generate_signed_certificate(ca_key, ca_cert, info: dict, cert_file: str, key_file: str, is_server: bool = False) -> tuple:
    """
    Generates a certificate signed by the CA.
    """
    # 1. Generate private key
    private_key = generate_private_key(key_file)
    
    # 2. Create subject
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, info["country"]),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, info["state"]),
        x509.NameAttribute(NameOID.LOCALITY_NAME, info["locality"]),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, info["organization"]),
        x509.NameAttribute(NameOID.COMMON_NAME, info["common_name"]),
    ])
    
    # 3. Build the certificate
    builder = (x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)  # Signed by CA
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=info["valid_days"]))
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
        .add_extension(x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=True,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False),
            critical=True))
    
    # 4. Add specific extensions for Server or Client
    if is_server:
        # Subject Alternative Name (SAN) is required by modern browsers/clients
        builder = builder.add_extension(
            x509.SubjectAlternativeName([x509.DNSName(info["common_name"])]),
            critical=False)
        # Extended Key Usage for Server Auth
        builder = builder.add_extension(
            x509.ExtendedKeyUsage([x509.OID_SERVER_AUTH]),
            critical=False)
    else:
        # Extended Key Usage for Client Auth
        builder = builder.add_extension(
            x509.ExtendedKeyUsage([x509.OID_CLIENT_AUTH]),
            critical=False)
    
    # 5. Sign the certificate with CA key
    cert = builder.sign(ca_key, hashes.SHA256(), default_backend())
    
    # 6. Save to file
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    return private_key, cert

def generate_all_certs():
    """Generates all necessary certificates (CA, Server, Client)."""
    if os.path.exists(CA_CERT_FILE):
        print("Certificates already exist. Delete them manually to regenerate.")
        return
    
    print("Generating all certificates...")
    ca_key, ca_cert = generate_ca_certificate()
    
    print("Generating server certificate...")
    generate_signed_certificate(ca_key, ca_cert, SERVER_INFO, SERVER_CERT_FILE, SERVER_KEY_FILE, is_server=True)
    
    print("Generating client certificate...")
    generate_signed_certificate(ca_key, ca_cert, CLIENT_INFO, CLIENT_CERT_FILE, CLIENT_KEY_FILE)
    
    print("All certificates generated successfully!")

# =============== SERVER FUNCTIONS ===============

def start_server(host: str):
    """
    Starts the SSL Server with Mutual Authentication.
    """
    # Configure SSL Context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED  # Enforce Client Authentication
    context.load_cert_chain(certfile=SERVER_CERT_FILE, keyfile=SERVER_KEY_FILE)
    context.load_verify_locations(cafile=CA_CERT_FILE)
    
    # Disable hostname check for local testing
    context.check_hostname = False
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, PORT))
        sock.listen(BACKLOG)
        print(f"Server listening on {host}:{PORT}")
        
        try:
            while True:
                conn, addr = sock.accept()
                print(f"Connection accepted from {addr}")
                
                try:
                    # Wrap the socket with SSL
                    with context.wrap_socket(conn, server_side=True) as ssl_conn:
                        # Retrieve and verify client certificate
                        cert = ssl_conn.getpeercert()
                        if not cert:
                            print("Warning: No client certificate received!")
                            continue
                        
                        subject = dict(x[0] for x in cert['subject'])
                        common_name = subject.get('commonName', 'Unknown')
                        print(f"Authenticated Client: {common_name}")
                        
                        # Receive data
                        data = ssl_conn.recv(BUFFER_SIZE)
                        if not data:
                            continue
                            
                        print(f"Received: {data.decode()}")
                        ssl_conn.sendall(b"Message received by server!")
                            
                except ssl.SSLError as e:
                    print(f"SSL Error during handshake: {e}")
                except Exception as e:
                    print(f"Communication Error: {e}")
                finally:
                    conn.close()
                        
        except KeyboardInterrupt:
            print("\nServer stopped by user.")

# =============== CLIENT FUNCTIONS ===============

def start_client(server_host: str):
    """
    Starts the SSL Client and connects to the server.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED  # Verify Server Certificate
    context.load_verify_locations(cafile=CA_CERT_FILE)
    context.load_cert_chain(certfile=CLIENT_CERT_FILE, keyfile=CLIENT_KEY_FILE)
    
    context.check_hostname = False
    
    try:
        with socket.create_connection((server_host, PORT)) as sock:
            print(f"Connected to {server_host}:{PORT}")
            
            with context.wrap_socket(sock, server_hostname=SERVER_INFO["common_name"]) as ssl_conn:
                cert = ssl_conn.getpeercert()
                subject = dict(x[0] for x in cert['subject'])
                common_name = subject.get('commonName', 'Unknown')
                print(f"Connected to server: {common_name}")
                
                message = b"Hello from client!"
                ssl_conn.sendall(message)
                print(f"Sent: {message.decode()}")
                
                data = ssl_conn.recv(BUFFER_SIZE)
                print(f"Response: {data.decode()}")
                
    except Exception as e:
        print(f"Connection error: {e}")

# =============== MAIN ENTRY POINT ===============

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Generate certs: python3 script.py gen_certs")
        print("  Start server:   python3 script.py server <address>")
        print("  Start client:   python3 script.py client <server_address>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "gen_certs":
        generate_all_certs()
    elif command == "server":
        host = sys.argv[2] if len(sys.argv) > 2 else '0.0.0.0'
        start_server(host)
    elif command == "client":
        if len(sys.argv) < 3:
            print("Please specify server address")
            sys.exit(1)
        start_client(sys.argv[2])
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()
