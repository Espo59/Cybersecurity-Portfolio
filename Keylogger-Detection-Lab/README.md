# Keylogger Detection & Endpoint Security Monitoring Lab

![Endpoint Security](https://img.shields.io/badge/Endpoint-Security-red?style=for-the-badge)
![Detection](https://img.shields.io/badge/Detection-Engineering-green?style=for-the-badge)
![SOC](https://img.shields.io/badge/SOC-Analysis-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Tool-Python-yellow?style=for-the-badge)

---

## 🧠 Executive Summary

This project simulates keylogger behavior and focuses on detecting it from an endpoint security and SOC perspective.

The goal is not only to demonstrate how keystroke logging works, but more importantly:
- How malicious input capture behavior can be detected
- What signals are generated on a system
- How SOC teams design detection rules for such threats

---

## ⚔️ Threat Model

Keyloggers are commonly used in malware for:

- Credential theft
- Sensitive data extraction
- Silent user monitoring

Attackers typically deploy them via:
- Phishing attachments
- Trojans
- Privilege escalation exploits

---

## 🧪 Behavior Simulation

The simulated keylogger demonstrates:

- Keyboard input capture
- Continuous background execution
- Data logging to local storage or memory buffer

This simulates typical malware behavior patterns used in credential theft attacks.

---

## 🧾 Observed Behavior

During execution, the following behaviors are relevant:

- Continuous input interception loop
- Persistent process activity
- Unusual background execution pattern
- Potential file access or logging activity

📁 Detailed analysis is documented in `/analysis.md`

---

## 🔍 Detection (SOC Perspective)

Detection is focused on behavioral indicators rather than signature-based rules.

### Endpoint-level indicators:
- Unauthorized keyboard input capture APIs
- Suspicious background processes
- Unexpected persistence mechanisms
- High-frequency input event hooks

### Detection engineering approaches:
- Process behavior monitoring (EDR)
- API call inspection (keyboard hook functions)
- Memory scanning for input capture routines
- Anomaly detection on user input handling

### SOC correlation:
- Correlating process behavior with input capture patterns
- Identifying non-standard input interception libraries
- Monitoring persistence after system startup

---

## 🛡 Limitations & Defensive Considerations

This simulation highlights key limitations:

- Simple keyloggers are hard to detect via static signatures
- Advanced variants use encryption and obfuscation
- Detection requires behavioral monitoring, not file scanning alone

### Mitigation strategies:
- Endpoint Detection & Response (EDR) tools
- Application whitelisting
- Privilege restriction policies
- Kernel-level input protection mechanisms

---

## 📁 Project Structure

```text
Keylogger-Detection-Lab/
├── detector.py
├── requirements.txt
├── docs/
│ ├── threat_model.md
│ ├── analysis.md
│ ├── soc_notes.md
│ └── limitations.md
└── README.md
```

---

## 🧠 Key Learning Outcomes

- Understanding keylogger behavior at system level
- Endpoint monitoring techniques
- Detection engineering principles (SOC mindset)
- Behavioral vs signature-based detection
- Limitations of traditional antivirus approaches

---

## 📌 Disclaimer

This project is intended for educational and cybersecurity research purposes in controlled environments only.

---

## 🏷️ Tags

`Keylogger` · `Endpoint Security` · `SOC Detection` · `Behavioral Analysis` · `Threat Monitoring` · `Cybersecurity Lab`
