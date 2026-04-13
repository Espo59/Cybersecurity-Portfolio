# ARP Poisoning & Man-in-the-Middle (MitM) Simulation
This repository contains a Python-based implementation of an ARP Spoofing attack, developed for educational purposes to demonstrate how the Address Resolution Protocol (ARP) can be manipulated within a local network.

---

# 🔍 Overview
ARP Spoofing is a technique where an attacker sends forged ARP messages onto a local area network. The goal is to associate the attacker's MAC address with the IP address of another host (such as the default gateway), causing any traffic meant for that IP to be sent to the attacker instead.

---

# 🛠 Features
- **Bi-directional Poisoning:** Simultaneously poisons the ARP cache of both the victim and the router to establish a full Man-in-the-Middle (MitM) position.

- **IP Forwarding Management:** Automatically enables IPv4 forwarding on the host machine to ensure the victim's connection is maintained during the attack.

- **Graceful Restoration:** Includes a dedicated cleanup function that restores the original ARP tables (re-healing the network) upon user interruption (Ctrl+C).

- **Real-time Monitoring:** Provides a live counter of the packets sent to maintain the "poisoned" state.

---

# 🚀 Lab Setup & Usage
**Prerequisites**
- **Operating System:** Linux (Kali Linux or Parrot OS recommended).

- **Libraries:** Scapy (pip install scapy).

- **Privileges:** Must be run as root to craft raw network packets.

**Execution**
- **Configure the script:** Open the file and update the following constants with your lab's IP/MAC addresses:

*VICTIM_IP / VICTIM_MAC*

*ROUTER_IP / ROUTER_MAC*

*ATTACKER_MAC*

**Run the attack:**


sudo python3 arp_spoofer.py

Observation: Use Wireshark on the attacker machine to observe the traffic flowing from the victim to the internet through your interface.

---

# 🧠 Educational Objectives
This experiment was conducted to understand:

The stateless nature of the ARP protocol and its lack of authentication.

How the sysctl kernel parameters affect network routing.

The importance of security measures like Dynamic ARP Inspection (DAI) and Static ARP tables in defending corporate networks.

---

# ⚠️ Disclaimer
FOR EDUCATIONAL PURPOSES ONLY.
This tool is intended for use in controlled, private laboratory environments for cybersecurity research and learning. Unauthorized use of this script on networks you do not own or have explicit permission to test is illegal. As a cybersecurity student, I advocate for ethical hacking and responsible disclosure.
