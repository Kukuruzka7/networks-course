import argparse
import socket


def check_port(ip_address, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)
        except Exception as e:
            print(f"Ошибка при проверке порта {port}: {str(e)}")
    return open_ports


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip_address', default='127.0.0.1')
    parser.add_argument('-start_port', type=int, default=5050)
    parser.add_argument('-end_port', type=int, default=5055)
    args = parser.parse_args()
    open_ports = check_port(args.ip_address, args.start_port, args.end_port)
    print("Свободный порты в промежутке", args.start_port, ":", args.end_port)
    for p in open_ports:
        print(p, sep=" ")
