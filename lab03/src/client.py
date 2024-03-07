import argparse
import socket
import sys


def send_get(server_host: str, server_port: int, filename: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        request = f"GET / HTTP/1.1\r\nContent-Type: application/json" \
                  f"\r\nHost: {server_host}:{server_port}\r\n" \
                  f"Content-Length: {len(filename.encode('utf-8'))}\r\n\r\n" \
                  f"{filename}"
        client_socket.sendall(request.encode())
        response = client_socket.recv(4096)
        print(response.decode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server_host')
    parser.add_argument('server_port')
    parser.add_argument('filename')
    args = parser.parse_args()
    send_get(args.server_host, int(args.server_port), args.filename)
