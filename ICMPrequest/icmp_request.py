#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sends a spoofed ICMP Echo Request (ping) using Scapy.
- Source IP:      192.168....
- Destination IP: 192.168....
- Interface:      eth0

Execution:
    sudo python3 ping_spoofed.py
"""

import os
import sys
from scapy.all import IP, ICMP, sr1, conf

# === Parameters =============================================================
SRC_IP  = ""  # The IP address you want to impersonate
DST_IP  = ""  # The target of the ping
IFACE   = "eth0"            # Network interface to use
TIMEOUT = 2                 # Seconds to wait for a response
TTL     = 64                # Time To Live for the IP packet
PAYLOAD = b"ping-test-scapy" # Optional data attached to the ICMP packet
# ============================================================================

def main():
    # Privilege check: raw socket creation requires root/admin privileges
    if hasattr(os, "geteuid") and os.getuid() != 0:
        print("[!] This script requires root privileges (sudo).")
        return 1

    # Reduce Scapy verbosity to keep the output clean
    conf.verb = 0

    # Build the IP Layer:
    # - src: The spoofed source IP address
    # - dst: The destination IP address
    # - ttl: Set to 64 (standard for Linux)
    ip_layer = IP(src=SRC_IP, dst=DST_IP, ttl=TTL)

    # Build the ICMP Layer:
    # - type=8: Specifies an 'Echo Request' (standard ping)
    # - id: Identifier to match requests with replies
    # - seq: Sequence number
    icmp_req = ICMP(type=8, id=0x1234, seq=1)

    # Stack the layers: IP / ICMP / Raw Payload
    packet = ip_layer / icmp_req / PAYLOAD

    print(f"[*] Sending spoofed ICMP Echo Request from {SRC_IP} to {DST_IP} on {IFACE}...")

    try:
        # sr1() sends the packet and waits for EXACTLY ONE response
        # Note: If the spoofing works, the response will likely go to the SRC_IP, 
        # not to this machine, causing a timeout here.
        response = sr1(packet, iface=IFACE, timeout=TIMEOUT)

        if response is None:
            print("[!] No response received (timeout).")
            print("    Potential causes: host down, ICMP filtering, anti-spoofing (uRPF), or incorrect routing.")
            return 2

        # Display the full details of the received packet
        print("[✓] Response received:")
        response.show()  
        print(f"[i] Summary: {response.summary()}")
        return 0

    except PermissionError:
        print("[!] Permission denied: please run with sudo.")
        return 3
    except OSError as e:
        print(f"[!] System error: {e}")
        return 4
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return 5

if __name__ == "__main__":
    sys.exit(main())
