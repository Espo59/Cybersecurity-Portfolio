#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to change the MAC address of a network interface on Linux
using the 'ip' command (iproute2 package). Requires root privileges.

Instructions:
1) Set INTERFACE and NEW_MAC in the constants below.
2) Run with: sudo python3 change_mac.py
"""

import re
import subprocess
import sys

# === PARAMETERS TO CUSTOMIZE ============================================
INTERFACE = "eth0"                 # e.g., "eth0", "wlan0", "enp3s0", etc.
NEW_MAC   = "00:11:22:33:44:58"    # format XX:XX:XX:XX:XX:XX
# ============================================================================


def run(cmd):
    """
    Executes a system command and raises an exception if it fails.
    - cmd: list of strings (e.g., ["ip", "link", "set", "eth0", "down"])
    Uses check=True to raise CalledProcessError in case of failure.
    """
    subprocess.run(cmd, check=True)


def get_current_mac(iface):
    """
    Returns the current MAC address of the interface 'iface'
    by reading the output of 'ip link show <iface>'.
    Returns None if not found.
    """
    try:
        out = subprocess.check_output(["ip", "link", "show", iface], text=True)
        m = re.search(r"link/ether\s+([0-9a-f:]{17})", out, re.IGNORECASE)
        if m:
            return m.group(1)
    except subprocess.CalledProcessError:
        pass
    return None


def is_valid_mac(addr):
    """
    Verifies that the string 'addr' is a valid MAC address in XX:XX:XX:XX:XX:XX format
    composed of hexadecimal digits.
    """
    return re.fullmatch(r"[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}", addr) is not None


def main():
    iface = INTERFACE
    new_mac = NEW_MAC

    # 1) Input validation
    if not iface:
        print("[!] Interface not specified.")
        return 1
    if not is_valid_mac(new_mac):
        print("[!] Invalid MAC: {} (use XX:XX:XX:XX:XX:XX format).".format(new_mac))
        return 1

    try:
        # 2) Current MAC (before modification)
        current_before = get_current_mac(iface)
        print("[i] Current MAC of {}: {}".format(iface, current_before))

        # 3) Bring the interface down to allow MAC change
        print("[+] Shutting down network interface {}...".format(iface))
        run(["ip", "link", "set", iface, "down"])

        # 4) Set the new MAC
        print("[+] Setting new MAC {} on {}...".format(new_mac, iface))
        run(["ip", "link", "set", iface, "address", new_mac])

        # 5) Bring the interface back up
        print("[+] Reactivating network interface {}...".format(iface))
        run(["ip", "link", "set", iface, "up"])

        # 6) Final verification
        current_after = get_current_mac(iface)
        print("[i] MAC reported by the system: {}".format(current_after))

        if current_after and current_after.lower() == new_mac.lower():
            print("[✓] MAC address changed successfully.")
            return 0
        else:
            print("[!] Warning: The MAC does not match the requested one.")
            print("    Possible causes: NetworkManager, drivers, or system policies.")
            return 2

    except subprocess.CalledProcessError as e:
        print("[!] System error during execution: {}".format(e))
        return 3
    except FileNotFoundError:
        print("[!] 'ip' command not found. Please install the 'iproute2' package.")
        return 4
    except Exception as e:
        print("[!] Unexpected error: {}".format(e))
        return 5


if __name__ == "__main__":
    sys.exit(main())
