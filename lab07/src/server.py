import random
import socket
import argparse


def receive(server_socket: socket, timeout: float = 1, receive_size: int = 1024):
    server_socket.settimeout(timeout)
    data, src_addr = None, None
    try:
        data, src_addr = server_socket.recvfrom(receive_size)
    except socket.timeout:
        pass
    except Exception as e:
        print("Error:", e)
    return data, src_addr


def run_server(port_number: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port_number))
    while 1:
        response, addr = receive(server_socket)
        if addr is not None:
            response = response.decode().upper().encode()
            if random.random() < 0.2:
                print("Packet loss simulated")
                continue
            server_socket.sendto(response, addr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('port_number')
    args = parser.parse_args()
    run_server(int(args.port_number))
