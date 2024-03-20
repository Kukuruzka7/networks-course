import argparse
import os
import socket
import base64


def send_email(receiver_email, subject, body):
    smtp_server = os.getenv("SERVER")
    port = int(os.getenv("PORT"))
    sender_email = os.getenv("MAIL")
    password = os.getenv("PASSWORD")

    with socket.create_connection((smtp_server, port)) as server_socket:
        print(server_socket.recv(1024).decode())

        server_socket.sendall(b"HELO example.com\r\n")
        print(server_socket.recv(1024).decode())

        server_socket.sendall(b"AUTH LOGIN\r\n")
        print(server_socket.recv(1024).decode())
        server_socket.sendall(base64.b64encode(sender_email.encode()) + b"\r\n")
        print(server_socket.recv(1024).decode())
        server_socket.sendall(base64.b64encode(password.encode()) + b"\r\n")
        print(server_socket.recv(1024).decode())

        server_socket.sendall(f"MAIL FROM:<{sender_email}>\r\n".encode())
        print(server_socket.recv(1024).decode())
        server_socket.sendall(f"RCPT TO:<{receiver_email}>\r\n".encode())
        print(server_socket.recv(1024).decode())
        server_socket.sendall(b"DATA\r\n")
        print(server_socket.recv(1024).decode())
        server_socket.sendall(f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n".encode())
        print(server_socket.recv(1024).decode())

        server_socket.sendall(b"QUIT\r\n")
        print(server_socket.recv(1024).decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('email')
    args = parser.parse_args()
    receiver_email = args.email
    subject = "Тестовое письмо"
    body = "Ура, отправилось!\nС уважением, Розалина\n"
    send_email(receiver_email, subject, body)
