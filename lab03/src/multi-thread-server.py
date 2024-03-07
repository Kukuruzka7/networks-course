from socket import *
import argparse
import threading
from time import sleep

base_path = "database/"


def handle_client(connection):
    # print("start handle client ", connection)
    file_path = base_path + connection.recv(1024).decode().split()[-1]
    try:
        with open(file_path, 'rb') as file:
            response = b"HTTP/1.1 200 OK\n\n" + file.read()
    except FileNotFoundError:
        response = b"HTTP/1.1 404 Not Found\n\nFile not found"
    connection.send(response)
    # sleep(10)
    # print("end handle client ", connection)
    connection.close()


def run_server(port_numbers: list[int]):
    main_port, *others = port_numbers
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("127.0.0.1", main_port))
    server_socket.listen(len(others))
    while 1:
        connection_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection_socket,))
        client_thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ports_nums", metavar="N", type=int, nargs="+", help="List of available ports")
    args = parser.parse_args()
    run_server(args.ports_nums)
