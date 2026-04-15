from scapy.all import IP, ICMP, TCP, sr1, sr, conf
import sys
from datetime import datetime

# Disable Scapy's verbose output
conf.verb = 0

def print_banner():
    """
    Prints the initial program banner
    """
    print("\n" + "="*60)
    print("     SYN SCANNER - AUTO DISCOVERY (1-65535)")
    print("="*60)

def icmp_probe(ip):
    """
    Checks if a host is reachable via an ICMP ping.
    
    Args:
        ip (str): The host IP address to verify
    
    Returns:
        bool: True if the host responds, False otherwise
    """
    print(f"\n[*] ICMP probe on {ip}...")
    
    # Create and send an ICMP Echo Request packet
    """
    This expression builds a stacked packet with an IP layer at the head and, 
    as its payload, an ICMP layer. In Scapy, the / operator is used to stack layers 
    on top of each other: the layer on the left is the higher-level header (IP here), 
    while the one on the right is the payload (ICMP here). The result is a single 
    Packet object containing both layers.

    What IP(dst=ip) does:
    IP() is the constructor for the IP layer (scapy.layers.inet.IP class).
    dst=ip sets the dst (destination IP) field to the address passed in the ip variable.
    If you don't specify other fields, Scapy initializes fields with default values 
    or with None for those that will be calculated automatically (e.g., checksum).
    Useful fields you can set: src, dst, ttl, id, tos, flags, chksum (usually left as 
    None so Scapy calculates it automatically on send).

    Example: IP(src="10.0.0.5", dst="8.8.8.8", ttl=64).

    What ICMP() does:
    ICMP() builds the ICMP layer (scapy.layers.inet.ICMP class).
    If you send ICMP() without parameters, you get an ICMP Echo Request by default 
    (typically type=8, code=0) — i.e., a "ping".

    You can specify fields like type, code, id, seq, etc.
    Example: ICMP(type=8, code=0, id=0x1234, seq=1) (Echo Request with id/seq).

    When the packet is sent, Scapy automatically calculates the ICMP checksum 
    if the chksum field is None.
    """
    icmp_packet = IP(dst=ip)/ICMP()
    # Send and wait for a response (ICMP or other)
    resp_packet = sr1(icmp_packet, timeout=2, verbose=0)
    
    if resp_packet is not None:
        print(f"[+] Host {ip} is reachable\n")
        return True
    else:
        print(f"[-] Host {ip} does not respond to ICMP ping")
        print(f"[*] Continuing scan anyway...\n")
        return False

def syn_scan(ip, port):
    """
    Performs a SYN scan on a single port.
    
    Args:
        ip (str): The target IP address
        port (int): The port to scan
    
    Returns:
        str: "open", "closed", or "filtered"
    """
    # Create a TCP SYN packet
    """
    Step-by-step breakdown:

    IP(dst=ip)
    Builds the IP layer (instance of scapy.layers.inet.IP).
    dst=ip sets the destination IP field.
    Other useful fields: src, ttl, id, tos. If not set, Scapy uses defaults or 
    calculates them at send time.

    TCP(dport=port, flags='S')
    Builds the TCP layer (instance of scapy.layers.inet.TCP).
    dport=port sets the destination port. Must be an integer (e.g., 80).
    flags='S' sets the TCP flags; here 'S' means SYN. Scapy accepts flags as 
    strings (e.g., 'S', 'SA', 'R') or numeric values (e.g., flags=0x02 for SYN).
    Other important TCP fields: sport (source port), seq, ack, window, options.

    The / operator between IP(...) and TCP(...)
    In Scapy, the / operator stacks layers: the left layer (IP) becomes the 
    outer header, the right one (TCP) the payload.

    What the resulting packet represents:
    syn_packet is a packet with:
    - IP Header towards ip
    - TCP Header with destination port and the SYN flag set
    It is the typical packet sent to initiate a TCP handshake (SYN). If the port 
    is open, the server normally responds with SYN+ACK (flags S+A, value 0x12). 
    If closed, it often responds with RST (reset, typically 0x14 if it includes ACK).
    """
    syn_packet = IP(dst=ip)/TCP(dport=port, flags='S')
    
    # Send packet and wait for response (1 second timeout)
    resp_packet = sr1(syn_packet, timeout=1, verbose=0)
    
    # Analyze the response
    if resp_packet is None:
        # No response = filtered port
        return "filtered"
    
    elif resp_packet.haslayer(TCP):
        # Extract TCP flags from response
        tcp_flags = resp_packet[TCP].flags
        
        # Flag 0x12 = SYN-ACK (port open)
        if tcp_flags == 0x12:
            # Send RST to close the connection
            """
            What it builds:
            IP(dst=ip) creates the IP layer.
            TCP(dport=port, flags='R') creates the TCP layer with the RST flag.
            The / operator stacks them.

            What the RST (Reset) flag means:
            A TCP packet with the RST flag terminates a connection abruptly.
            In a SYN scan, after receiving SYN+ACK, the scanner sends a RST 
            to avoid completing the handshake ("half-open" mode). This leaves 
            fewer application logs.
            """
            rst_packet = IP(dst=ip)/TCP(dport=port, flags='R', seq=int(resp_packet[TCP].ack))
            sr1(rst_packet, timeout=1, verbose=0)
            return "open"
        
        # Flag 0x14 = RST-ACK (port closed)
        elif tcp_flags & 0x04:  # Check if RST is set
            return "closed"
    
    # Other cases = filtered port
    return "filtered"

def quick_scan(ip, start_port=1, end_port=1024, batch_size=100):
    """
    Rapidly scans a range of ports to find open ones.
    Uses batches to speed up (sends multiple packets together).
    
    Args:
        ip (str): Target IP
        start_port (int): First port of the range
        end_port (int): Last port of the range
        batch_size (int): Number of ports to scan per batch
    
    Returns:
        list: List of open ports
    """
    open_ports = []
    total_ports = end_port - start_port + 1
    scanned = 0
    
    print(f"[*] Quick scan on ports {start_port}-{end_port}...")
    print(f"[*] Total ports: {total_ports}")
    print(f"[*] This might take a few minutes...\n")
    
    # Scan in batches to speed up
    for batch_start in range(start_port, end_port + 1, batch_size):
        batch_end = min(batch_start + batch_size - 1, end_port)
        
        # Create SYN packets for all ports in the batch
        packets = [
            IP(dst=ip)/TCP(dport=port, flags='S') 
            for port in range(batch_start, batch_end + 1)
        ]
        
        # Send all packets and receive responses
        # inter=0.001 = 1ms between packets (prevents overload)
        answered, unanswered = sr(packets, timeout=2, verbose=0, inter=0.001)
        
        # Analyze responses
        """
        Detailed explanation:

        for sent, received in answered:
        answered is the result of sr() or sr1(). It's a list of 
        (sent_packet, received_packet) pairs.

        if received.haslayer(TCP):
        Checks if the response contains a TCP layer.

        if received[TCP].flags == 0x12: # SYN-ACK
        Checks if flags are exactly SYN+ACK (0x12).

        port = received[TCP].sport
        Gets the source port of the received packet (the port on the target).
        
        Building the RST:
        rst = IP(dst=ip)/TCP(dport=port, flags='R')
        Sends a Reset to close the "half-open" connection.
        """
        for sent, received in answered:
            if received.haslayer(TCP):
                # If SYN-ACK is received, port is open
                if received[TCP].flags == 0x12:  # SYN-ACK
                    port = received[TCP].sport
                    open_ports.append(port)
                    print(f"[+] Port {port:5d} OPEN")
                    
                    # Send RST to close the connection
                    rst = IP(dst=ip)/TCP(dport=port, flags='R')
                    sr1(rst, timeout=1, verbose=0)
        
        # Update progress
        scanned += (batch_end - batch_start + 1)
        percentage = (scanned / total_ports) * 100
        print(f"[*] Progress: {scanned}/{total_ports} ({percentage:.1f}%)", end='\r')
    
    print("\n")  # New line after progress
    return sorted(open_ports)

def full_scan(ip, ports):
    """
    Performs a detailed scan on specified ports.
    
    Args:
        ip (str): Target IP
        ports (list): List of ports to scan in detail
    """
    print("\n" + "="*60)
    print("     DETAILED SCAN OF OPEN PORTS")
    print("="*60 + "\n")
    
    results = {"open": [], "closed": [], "filtered": []}
    
    for port in ports:
        print(f"[*] Detailed analysis of port {port}...", end='')
        status = syn_scan(ip, port)
        results[status].append(port)
        
        # ANSI color coding
        if status == "open":
            print(f" [\033[92mOPEN\033[0m]")
        elif status == "closed":
            print(f" [\033[91mCLOSED\033[0m]")
        else:
            print(f" [\033[93mFILTERED\033[0m]")
    
    return results

def print_summary(results, start_time):
    """
    Prints the final scan summary.
    
    Args:
        results (dict): Dictionary with scan results
        start_time (datetime): Scan start timestamp
    """
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*60)
    print("     SCAN SUMMARY")
    print("="*60 + "\n")
    
    # Open ports
    if results["open"]:
        print(f"[+] OPEN Ports ({len(results['open'])}):")
        for port in results["open"]:
            print(f"    - Port {port}")
    else:
        print("[-] No open ports found")
    
    print()
    
    # Closed ports
    if results["closed"]:
        print(f"[-] CLOSED Ports ({len(results['closed'])}):")
        for port in results["closed"]:
            print(f"    - Port {port}")
    
    print()
    
    # Filtered ports
    if results["filtered"]:
        print(f"[?] FILTERED Ports ({len(results['filtered'])}):")
        for port in results["filtered"]:
            print(f"    - Port {port}")
    
    print("\n" + "="*60)
    print(f"[*] Total time: {duration:.2f} seconds")
    print("="*60 + "\n")

def main():
    """
    Main program function
    """
    # Check arguments
    if len(sys.argv) < 2:
        print("\n[!] Correct Usage:")
        print("    sudo python3 syn_scanner_auto.py <IP> [options]\n")
        print("Options:")
        print("    --quick       Scan only ports 1-1024 (fast)")
        print("    --common      Scan only top 100 common ports")
        print("    --full        Scan all 65535 ports (slow)\n")
        print("Examples:")
        print("    sudo python3 syn_scanner_auto.py 192.168.1.1 --quick")
        print("    sudo python3 syn_scanner_auto.py 192.168.1.1 --full")
        print("    sudo python3 syn_scanner_auto.py 192.168.1.1  (default: --quick)\n")
        sys.exit(1)
    
    # Extract IP and options
    ip = sys.argv[1]
    
    # Determine port range
    if "--full" in sys.argv:
        start_port = 1
        end_port = 65535
        scan_type = "FULL (1-65535)"
    elif "--common" in sys.argv:
        # List of the top 100 most common ports
        common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 
            995, 1723, 3306, 3389, 5900, 8080, 20, 69, 161, 162, 389, 636, 
            1433, 1521, 2049, 3268, 5432, 5800, 8443, 1080, 1194, 8888, 27017,
            137, 138, 500, 1701, 4500, 465, 587, 514, 515, 631, 873, 2181,
            2375, 2376, 3000, 5000, 5001, 5432, 5984, 6379, 7001, 8000, 8008,
            8081, 8443, 8888, 9000, 9090, 9200, 9300, 10000, 27017, 28017,
            50000, 50070, 123, 161, 162, 179, 389, 443, 636, 989, 990, 1433,
            1434, 1521, 1830, 2082, 2083, 2086, 2087, 2095, 2096, 3128, 8009,
            9999, 19132, 19133, 25565, 25575
        ][:100]
        print(f"[*] Mode: Common ports scan")
        start_time = datetime.now()
        print_banner()
        print(f"Target: {ip}")
        print(f"Scan type: COMMON PORTS (top 100)\n")
        
        # Ping check
        icmp_probe(ip)
        
        # Scan common ports only
        open_ports = []
        for port in common_ports:
            status = syn_scan(ip, port)
            if status == "open":
                open_ports.append(port)
                print(f"[+] Port {port:5d} OPEN")
        
        if open_ports:
            results = full_scan(ip, open_ports)
            print_summary(results, start_time)
        else:
            print("[-] No common open ports found")
        
        return
    else:  # Default: --quick
        start_port = 1
        end_port = 1024
        scan_type = "QUICK (1-1024)"
    
    # Print initial information
    start_time = datetime.now()
    print_banner()
    print(f"Target: {ip}")
    print(f"Scan type: {scan_type}")
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Verify host is reachable
    icmp_probe(ip)
    
    # Step 2: Quick scan to find open ports
    open_ports = quick_scan(ip, start_port, end_port)
    
    # Step 3: If open ports are found, do detailed scan
    if open_ports:
        print(f"\n[+] Found {len(open_ports)} open ports")
        print(f"[*] Starting detailed scan...\n")
        
        results = full_scan(ip, open_ports)
        print_summary(results, start_time)
    else:
        print(f"[-] No open ports found in range {start_port}-{end_port}")
        print(f"[*] Total time: {(datetime.now() - start_time).total_seconds():.2f} seconds\n")

# Program entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(0)
    except PermissionError:
        print("\n[!] Error: Insufficient privileges")
        print("[!] Run the program with root/administrator privileges")
        print("[!] Linux/Mac: sudo python3 syn_scanner_auto.py <IP>")
        print("[!] Windows: Run as Administrator\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
