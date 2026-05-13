# 🛰️ Detection Techniques

## Indicators of ARP Spoofing

- Multiple IP addresses mapped to the same MAC
- Frequent ARP table changes
- Unusual ARP reply traffic

---

## Detection Methods

### 1. Network Monitoring

Tools like Wireshark can reveal:
- Duplicate ARP responses
- Unexpected MAC changes

---

### 2. Switch-Level Protection

- Dynamic ARP Inspection (DAI)
- DHCP Snooping

---

### 3. Host-Based Detection

- Monitor ARP cache changes
- Use tools like arpwatch

---

## SOC Perspective

ARP spoofing is often part of a larger attack chain and should trigger further investigation.
