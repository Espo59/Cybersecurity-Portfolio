# ARP Spoofing (MITM Attack Simulation & Detection Lab)

![Network Security](https://img.shields.io/badge/Network-Security-red?style=for-the-badge&logo=proxmox)
![MITM](https://img.shields.io/badge/Attack-MITM-orange?style=for-the-badge)
![Scapy](https://img.shields.io/badge/Tool-Scapy-blue?style=for-the-badge)
![Detection](https://img.shields.io/badge/SOC-Detection-green?style=for-the-badge)

---

## 🧠 Executive Summary

This project simulates an ARP Spoofing (Man-in-the-Middle) attack in a controlled environment using Scapy.

The objective is to demonstrate:
- How ARP cache poisoning enables traffic interception
- How a MITM position is established at network level
- How this attack can be detected from a SOC perspective
- How mitigation techniques can prevent ARP-based attacks

---

## ⚔️ Attack Overview

ARP Spoofing works by exploiting the lack of authentication in the ARP protocol.

An attacker sends forged ARP replies to:
- Associate their MAC address with the victim’s IP
- Poison the ARP cache of target devices
- Intercept traffic between victim and gateway

This results in a Man-in-the-Middle (MITM) position.

---

## 🧪 Attack Implementation

The attack is implemented using Scapy to:

- Continuously send spoofed ARP responses
- Impersonate the network gateway
- Redirect traffic through the attacker machine

Script:
- `arp_spoof_and_leave.py`

---

## 🧾 Evidence (Network Behavior)

During the attack, the following behaviors can be observed:

- ARP cache changes on victim machine
- Gateway IP mapped to attacker MAC address
- Traffic routed through attacker system
- Increased ARP reply frequency

📁 Screenshots and packet captures can be analyzed using Wireshark to observe:
- ARP reply anomalies
- MAC address inconsistencies
- Traffic redirection patterns

---

## 🔍 Detection (SOC Perspective)

ARP Spoofing can be detected using:

### Network Indicators:
- Multiple ARP replies for the same IP from different MACs
- Sudden changes in ARP cache entries
- Gateway MAC address inconsistency

### Detection Techniques:
- ARP inspection (Dynamic ARP Inspection - DAI)
- Network monitoring tools (Wireshark, Zeek)
- IDS rules detecting ARP anomalies

### SOC Correlation:
- Unusual L2 traffic patterns
- Gateway impersonation detection
- Cross-device MAC/IP mismatches

---

## 🛡 Mitigation

To prevent ARP spoofing attacks:

- Enable Dynamic ARP Inspection (DAI)
- Use static ARP entries for critical systems
- Segment network (VLAN isolation)
- Monitor ARP tables for anomalies
- Use encrypted protocols (HTTPS, SSH) to reduce MITM impact

---

## 📁 Project Structure

```text
ArpSpoofAndLeave/
├── arp_spoof_and_leave.py
├── docs/
│ ├── attack_analysis.md
│ ├── detection.md
│ └── mitigation.md
└── README.md
```

---

## 🧠 Key Learning Outcomes

- ARP protocol weaknesses and exploitation
- Man-in-the-Middle attack mechanics
- Network packet manipulation using Scapy
- SOC-level detection of L2 attacks
- Defensive mitigation strategies in enterprise networks

---

## 📌 Disclaimer

This project is for educational purposes only and demonstrates a controlled network security simulation. It must not be used on unauthorized networks.

---

## 🏷️ Tags

`ARP Spoofing` · `MITM Attack` · `Network Security` · `Scapy` · `Traffic Interception` · `SOC Detection` · `LAN Security`

This project is released under the MIT License.
