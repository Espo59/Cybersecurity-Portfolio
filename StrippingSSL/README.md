# MitM Automator: SSL Stripping & HSTS Hijack
This Python script is an automation wrapper for Bettercap, designed to perform sophisticated Man-in-the-Middle (MitM) attacks.
It simplifies the deployment of traffic interception tools to analyze how encrypted web traffic can be downgraded and inspected.

---

# 🔍 How It Works
The tool orchestrates a multi-stage attack by injecting specific commands into the Bettercap engine to bypass modern web security protocols.

**ARP Cache Poisoning:** The script initiates an ARP spoofing attack, positioning the auditor's machine as the "Man-in-the-Middle" 
between the target host and the gateway.

**SSL Stripping:** It enables a transparent HTTP proxy that intercepts HTTPS requests. By modifying the traffic in real-time, 
it attempts to force the victim's browser to communicate over unencrypted HTTP.

**HSTS Hijacking:** Utilizing the hstshijack caplet, the tool targets the "Strict Transport Security" policy by spoofing DNS responses and stripping security headers, tricking the browser into bypassing its safety checks.

**Packet Sniffing & Parsing:** Once the traffic is downgraded, the script activates a sniffer to capture sensitive data, such as plaintext credentials, session cookies, and visited URLs.

---

# 🛠 Features
- **Automated Workflow:** Replaces manual Bettercap console input with a single-command execution.

- **HSTS Bypass:** Integrated support for hstshijack to counter modern browser security.

- **Smart Noise Reduction:** Automatically filters out system events (zeroconf, endpoint discovery) for a cleaner data stream.

- **Virtualization Guard:** Specifically designed to ignore traffic from the virtualization host (e.g., VMware/VirtualBox) to maintain lab stability.

- **Graceful Cleanup:** Ensures that all Bettercap modules are properly disabled upon termination (SIGINT).

---

# 🧪 Educational Objectives
This project was developed to explore:

The inherent vulnerabilities of the ARP Protocol.

The mechanics of SSL/TLS Downgrade attacks.

The effectiveness (and limitations) of HSTS in protecting web users.

The practical application of Python's subprocess module for security tool orchestration.

---

# 🚀 Usage
**Prerequisites:**
Linux OS (Kali Linux or Parrot OS highly recommended).

Bettercap v2.x and the hstshijack caplet installed.

Root Privileges (Required for network socket manipulation and packet injection).

**Installation:**
Bash
*Update Bettercap and install the necessary caplets*
sudo bettercap -eval "caplets.update; q"

**Execution**
Configure the TARGET_IP and INTERFACE inside the script.

**Run the automator:**
Bash
sudo python3 mitm_strip.py

---

# ⚠️ Disclaimer
FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY. This tool is intended for use in controlled laboratory environments. Unauthorized interception of network traffic is illegal and unethical. Always obtain explicit, written permission before performing any security assessment or network audit.
