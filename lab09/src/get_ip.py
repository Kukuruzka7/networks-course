import ipaddress
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('196.0.0.0', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


ip = get_ip()
print("IP адрес:", get_ip())
print("Маска сети: v4", ipaddress.IPv4Network(ip).netmask)
