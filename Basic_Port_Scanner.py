import socket
from concurrent.futures import ThreadPoolExecutor

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def scan_port(ip, port):
    """Attempts to connect to a given IP and port using TCP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)  # Faster response
        result = s.connect_ex((ip, port))
        if result == 0:
            return port
    return None

def main():
    print("=== Basic Port Scanner ===")
    
    ip = input("Enter target IP address: ").strip()
    if not is_valid_ip(ip):
        print("[!] Invalid IP address.")
        return

    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            raise ValueError
    except ValueError:
        print("[!] Invalid port range. Ports must be between 1 and 65535.")
        return

    print(f"\n[*] Scanning {ip} from port {start_port} to {end_port}...\n")
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            port = future.result()
            if port:
                open_ports.append(port)

    if open_ports:
        print("[+] Open Ports:")
        for port in open_ports:
            print(f" - Port {port} is OPEN")
    else:
        print("[-] No open ports found in the given range.")

if __name__ == "__main__":
    main()
