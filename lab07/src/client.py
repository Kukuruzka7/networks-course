from datetime import datetime
import socket
import argparse

times = []


def send(client_socket, address, index, timeout: float = 1):
    client_socket.settimeout(timeout)
    start_time = datetime.now()
    time_for_print = start_time.strftime("%H:%M:%S.%f")
    try:
        client_socket.sendto(f"Ping {index} {time_for_print}".encode(), address)
        response, _ = client_socket.recvfrom(1024)
        end_time = datetime.now()
        rtt = end_time - start_time
        print(response.decode(), "RTT: ", rtt.microseconds / 1e6)
        times.append(rtt.microseconds / 1e6)
    except socket.timeout:
        print("Request timed out")
    except Exception as e:
        print("Error:", e)


def send_10(address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(1, 11):
        send(client_socket, address, i)
        if len(times) == 0:
            packet_loss = (i - len(times)) / 10 * 100
            print(f'Packet Loss: {packet_loss:.1f}%')
        else:
            min_rtt = min(times)
            max_rtt = max(times)
            mean_rtt = sum(times) / len(times)
            packet_loss = (i - len(times)) / i * 100
            print(f'Minimum RTT: {min_rtt:.6f} seconds')
            print(f'Maximum RTT: {max_rtt:.6f} seconds')
            print(f'Average RTT: {mean_rtt:.6f} seconds')
            print(f'Packet Loss: {packet_loss:.1f}%')
    client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server_host')
    parser.add_argument('server_port')
    args = parser.parse_args()
    server_address = (args.server_host, int(args.server_port))
    send_10(server_address)
