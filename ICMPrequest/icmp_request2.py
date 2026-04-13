#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sends a spoofed ICMP Echo Request and provides a detailed forensic report
explaining each field of the IP and ICMP headers.

Perfect for learning network protocols and packet structure.
"""

import os
import sys
from scapy.all import IP, ICMP, sr1, conf, hexdump

# === Configuration ===
SRC_IP  = ""
DST_IP  = ""
IFACE   = "eth0"
TIMEOUT = 2
TTL     = 64
PAYLOAD = b"ping-test-scapy"
# =====================

def explain_ip(ip):
    """Provides a detailed explanation of the IP Header fields."""
    lines = [f"--- IP Layer (Internet Protocol v{ip.version}) ---"]
    lines.append(f"  version = {ip.version} -> Protocol version (4 for IPv4).")
    lines.append(f"  ihl     = {ip.ihl} -> Header Length (in 32-bit words).")
    lines.append(f"  tos     = {ip.tos:#x} -> Type of Service (Priority/ECN).")
    lines.append(f"  len     = {ip.len} bytes -> Total packet length (Header + Data).")
    lines.append(f"  id      = {ip.id} -> Identification: Used for reassembling fragmented packets.")
    
    # Flags Handling
    df = bool(ip.flags.DF) if hasattr(ip.flags, "DF") else bool(ip.flags & 0x2)
    mf = bool(ip.flags.MF) if hasattr(ip.flags, "MF") else bool(ip.flags & 0x1)
    lines.append(f"  flags   = {ip.flags} -> [DF: {int(df)}, MF: {int(mf)}] (Don't Fragment / More Fragments).")
    
    lines.append(f"  frag    = {ip.frag} -> Fragment offset. 0 if not fragmented.")
    lines.append(f"  ttl     = {ip.ttl} -> Time To Live: Max hops before the packet is dropped.")
    lines.append(f"  proto   = {ip.proto} -> Upper layer protocol (1=ICMP, 6=TCP, 17=UDP).")
    lines.append(f"  src     = {ip.src} -> Spoofed Source IP.")
    lines.append(f"  dst     = {ip.dst} -> Target Destination IP.")
    return "\n".join(lines)

def explain_icmp(icmp):
    """Provides a detailed explanation of the ICMP Header fields."""
    lines = ["--- ICMP Layer (Internet Control Message Protocol) ---"]
    lines.append(f"  type    = {icmp.type} -> Message type (0=Echo Reply, 8=Echo Request).")
    lines.append(f"  code    = {icmp.code} -> Sub-code (0 for Echo messages).")
    lines.append(f"  chksum  = {icmp.chksum:#x} -> Checksum to verify header integrity.")
    if hasattr(icmp, "id"):
        lines.append(f"  id      = {icmp.id} -> Echo ID: Matches requests with replies.")
    if hasattr(icmp, "seq"):
        lines.append(f"  seq     = {icmp.seq} -> Sequence number: Tracks the packet order.")
    return "\n".join(lines)

def main():
    if hasattr(os, "geteuid") and os.geteuid() != 0:
        print("[!] Root privileges required.")
        return 1

    conf.verb = 0
    packet_out = IP(src=SRC_IP, dst=DST_IP, ttl=TTL) / ICMP(type=8, id=0x1234, seq=1) / PAYLOAD

    print(f"[*] Sending Detailed ICMP Request to {DST_IP}...")

    try:
        response = sr1(packet_out, iface=IFACE, timeout=TIMEOUT)

        if response is None:
            print("[!] Timeout: No response. The spoofed IP might be filtered or host is down.")
            return 2

        print("[✓] Response Captured! Forensic breakdown:\n")
        
        if response.haslayer(IP): print(explain_ip(response[IP]))
        print()
        if response.haslayer(ICMP): print(explain_icmp(response[ICMP]))
        print("\n--- Raw Hexdump ---")
        hexdump(response)

        return 0
    except Exception as e:
        print(f"[!] Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
