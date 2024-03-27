import argparse
from ftplib import FTP
import os


def ls(ftp):
    files = []
    ftp.dir(files.append)
    for f in files:
        print(f)


def download(ftp, filename):
    with open(filename, 'wb') as local_file:
        ftp.retrbinary('RETR ' + filename, local_file.write)


def upload(ftp, filename):
    with open(filename, 'rb') as local_file:
        ftp.storbinary('STOR ' + os.path.basename(filename), local_file)


def run_app(ftp):
    while True:
        command = input("Введите команду (ls, download, upload, exit): ")
        if command == 'ls':
            ls(ftp)
        elif command == 'exit':
            break
        else:
            command, filename = command.split(" ")
            if command == 'download':
                try:
                    download(ftp, filename)
                    print(f"Файл '{filename}' успешно скачан с сервера.")
                except Exception as e:
                    print(str(e))
                    continue
            elif command == 'upload':
                try:
                    upload(ftp, filename)
                    print(f"Файл '{filename}' успешно загружен на сервера.")
                except Exception as e:
                    print(str(e))
                    continue
            else:
                print("Неверная команда. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server')
    parser.add_argument('port')
    parser.add_argument('username')
    parser.add_argument('-password')
    args = parser.parse_args()
    server = args.server
    port = int(args.port)
    username = args.username
    password = "" if args.password is None else args.password
    ftp = FTP()
    try:
        ftp.connect(server, port)
        ftp.login(username, password)
        run_app(ftp)
    except Exception as e:
        print(str(e))
    finally:
        ftp.close()
