from socket import *
import argparse

base_path = "database/"


def run_server(port_number: int):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', port_number))
    server_socket.listen(1)
    while 1:
        connection_socket, addr = server_socket.accept()
        file_path = base_path + connection_socket.recv(1024).decode().split()[-1]
        try:
            with open(file_path, 'rb') as file:
                response = b"HTTP/1.1 200 OK\n\n" + file.read()
        except FileNotFoundError:
            response = b"HTTP/1.1 404 Not Found\n\nFile not found"
        connection_socket.send(response)
        connection_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('port_number')
    args = parser.parse_args()
    run_server(int(args.port_number))
