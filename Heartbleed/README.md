# Heartbleed (CVE-2014-0160) — Memory Disclosure in OpenSSL

![CVE](https://img.shields.io/badge/CVE-2014--0160-critical?style=for-the-badge&logo=openssl&logoColor=white)
![OpenSSL](https://img.shields.io/badge/OpenSSL-Vulnerable-red?style=for-the-badge&logo=openssl)
![TLS](https://img.shields.io/badge/TLS-Protocol_Attack-orange?style=for-the-badge)
![Type](https://img.shields.io/badge/Security-Lab-blue?style=for-the-badge)

## 🧠 Executive Summary

This project simulates the exploitation and analysis of the Heartbleed vulnerability (CVE-2014-0160), a critical flaw in the OpenSSL TLS heartbeat extension that allows remote memory disclosure.

The objective of this lab is to demonstrate:
- How the vulnerability is exploited at protocol level
- How sensitive memory data can be leaked from a remote server
- How such activity can be detected from a defensive (SOC) perspective
- How the vulnerability is mitigated in modern TLS implementations

---

## ⚔️ Vulnerability Overview

Heartbleed is caused by improper bounds checking in the TLS heartbeat extension.  
A malicious client can send a crafted heartbeat request with a payload length larger than the actual data provided.

As a result, the server responds with additional memory contents beyond the intended buffer.

This can lead to leakage of:
- Session keys
- User credentials
- Private server memory data
- Internal application information

---

## 🧪 Exploitation

This project includes multiple exploit implementations demonstrating progressive refinement of the attack:

- `heartbleedv2.py` → initial proof-of-concept exploit
- `heartbleedv3.py` → improved memory extraction reliability
- `heartbleed3v2.py` → refined payload control and response parsing

These scripts simulate malformed heartbeat requests to extract memory from a vulnerable TLS service.

---

## 🧾 Evidence of Exploitation

The exploit demonstrates successful memory leakage from the TLS server by requesting oversized heartbeat payloads.

Observed behavior includes:
- Response packets containing non-initialized memory regions
- Repeated leakage of server-side memory chunks
- Exposure of random but sensitive-looking binary data

This behavior is consistent with CVE-2014-0160 exploitation patterns.

---

## 🔍 Detection (SOC Perspective)

From a defensive standpoint, Heartbleed exploitation can be identified through:

### Network-level indicators:
- TLS heartbeat requests with abnormal payload sizes
- Repeated heartbeat requests with inconsistent lengths
- Server responses returning unexpected memory content sizes

### Security monitoring:
- IDS/IPS signatures targeting CVE-2014-0160 patterns
- TLS anomaly detection in heartbeat extension usage
- Traffic inspection for oversized heartbeat responses

### SOC correlation:
- Correlating unusual TLS traffic spikes with session metadata leakage attempts
- Monitoring repeated handshake/session renegotiation patterns

---

## 🛡 Mitigation

The vulnerability can be mitigated through:

- Upgrading OpenSSL to version ≥ 1.0.1g (patched version)
- Disabling TLS heartbeat extension if not required
- Implementing strict bounds checking on all memory copy operations
- Using modern TLS libraries with verified security patches
- Continuous patch management in production environments

---

## 📊 Security Impact

Heartbleed was one of the most critical TLS vulnerabilities ever discovered because it:
- Affected a large portion of internet-facing services
- Required no authentication to exploit
- Allowed silent memory extraction without detection in many cases

---

## 📁 Project Structure

```text
heartbleed/
├── heartbleedv2.py
├── heartbleedv3.py
├── heartbleed3v2.py
├── docs/
│ ├── vulnerability.md
│ ├── impact.md
│ └── detection_mitigation.md
└── README.md
```

---

## 📚 Technical Deep Dive

For a more detailed analysis of the vulnerability, impact, and defensive strategies, see the `/docs` folder.

---

## 🧠 Key Learning Outcomes

- Understanding TLS protocol internals (heartbeat extension)
- Memory disclosure vulnerability class (buffer over-read)
- Exploit development methodology for CVEs
- SOC-level detection strategies for protocol abuse
- Real-world mitigation and patch management practices

---

## 📌 Disclaimer

This project is for educational and security research purposes only.  
It simulates a known vulnerability in a controlled environment and must not be used against unauthorized systems.

---

## 🏷️ Tags

`CVE-2014-0160` · `OpenSSL` · `TLS Security` · `Memory Disclosure` · `Exploit Development` · `SOC Analysis` · `Network Security`
