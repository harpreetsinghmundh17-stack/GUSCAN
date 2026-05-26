print("""
 ██████╗ ██╗   ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
██╔════╝ ██║   ██║██╔════╝██╔════╝██╔══██╗████╗  ██║
██║  ███╗██║   ██║███████╗██║     ███████║██╔██╗ ██║
██║   ██║██║   ██║╚════██║██║     ██╔══██║██║╚██╗██║
╚██████╔╝╚██████╔╝███████║╚██████╗██║  ██║██║ ╚████║
 ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
        Port Scanner v1.0 | Made by You
""")
import socket
import concurrent.futures
import sys

def scan_port(host, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                print(f"  [OPEN] Port {port} --> {service}")
                return port
    except Exception:
        return None

def scan_ports(host, start=1, end=1024, threads=100):
    print(f"Scanning {host} (ports {start}-{end})...\n")
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, host, p): p for p in range(start, end + 1)}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)

    open_ports.sort()
    print(f"\nDone. {len(open_ports)} open port(s) found.")
    return open_ports

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
scan_ports(host, start=1, end=1024)
