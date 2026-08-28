# port_scanner.py

import socket
from concurrent.futures import ThreadPoolExecutor


COMMON_PORTS = {
    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-ALT"
}


def scan_port(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return port
    except:
        pass
    finally:
        sock.close()

    return None


def scan_host(host):

    print("=" * 60)
    print("NITRON PORT SCANNER")
    print("=" * 60)
    print(f"Target: {host}")
    print()

    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:

        results = executor.map(
            lambda p: scan_port(host, p),
            COMMON_PORTS.keys()
        )

    for port in results:
        if port:
            open_ports.append(port)

    if not open_ports:
        print("No common open ports found.")
    else:
        print("Open Ports")
        print("-" * 60)

        for port in sorted(open_ports):
            print(f"{port:<6} {COMMON_PORTS[port]}")

    print("=" * 60)

    return open_ports


if __name__ == "__main__":

    host = input("Host (default localhost): ").strip()

    if host == "":
        host = "127.0.0.1"

    scan_host(host)
