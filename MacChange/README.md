# Python MAC Address Changer
A lightweight, robust Python utility designed for Linux systems to modify the Media Access Control (MAC) address of network interfaces using the iproute2 suite.

---

# 🌟 Features
- Automatic Interface Management: Automatically handles bringing the interface down and up to apply changes.

- Validation: Built-in Regex validation to ensure the new MAC address follows the XX:XX:XX:XX:XX:XX format.

- Verification: Performs a post-execution check to confirm the system has successfully applied the new hardware address.

- Safety First: Includes comprehensive error handling for missing permissions (root), invalid interfaces, or missing system dependencies.

---

# 🚀 Installation & Requirements
- Operating System: Linux (requires the ip command, usually part of the iproute2 package).

- Privileges: Must be run with root/sudo privileges to modify hardware settings.

- Python: Compatible with Python 3.6+.

No external Python libraries are required (uses standard libraries: re, subprocess, sys).

---

# 🛠 Usage
- Clone the repository:

git clone https://github.com/yourusername/mac-changer.git
cd mac-changer

- Configure the script:
Open change_mac.py and edit the constants at the top:

INTERFACE = "eth0"                 # Your target interface
NEW_MAC   = "00:11:22:33:44:58"    # Your desired MAC

- Run with sudo:

sudo python3 change_mac.py

---

# 🔍 How it works
The script follows a standard 4-step networking procedure:

Scan: Retrieves and displays the current MAC address.

Disable: Shuts down the target interface (ip link set <iface> down).

Modify: Changes the hardware address (ip link set <iface> address <mac>).

Enable: Brings the interface back online (ip link set <iface> up).

---

# ⚠️ Disclaimer
Educational and Testing Purposes Only.
Changing your MAC address can be used for privacy or network testing. However, ensure you comply with your local laws and network policies. The author is not responsible for any misuse or disruption of network services.

---

# 📜 License
Distributed under the MIT License. See LICENSE for more information.
