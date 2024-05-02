import socket
import struct
import time
import numpy as np


def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + (data[i + 1])
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF
    return checksum


def my_ping(addr, icmp_seq):
    icmp = socket.getprotobyname("icmp")
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    icmp_socket.settimeout(1)

    icmp_type = 8  # Тип ICMP-сообщения (эхо-запрос)
    icmp_code = 0  # Код ICMP-сообщения
    icmp_id = 1000  # Идентификатор пакета
    icmp_checksum = calculate_checksum(struct.pack('!BBHHH', icmp_type, icmp_code, 0, icmp_id, icmp_seq))
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    try:
        start_time = time.time()
        icmp_socket.sendto(icmp_header, addr)
        reply, _ = icmp_socket.recvfrom(1024)
        end_time = time.time()
        rtt = (end_time - start_time) * 1000
        resp_type, resp_code = struct.unpack('!BB', reply[20:22])
        if resp_type == 0 and resp_code == 0:
            return rtt, "Success"
        if resp_type == 3:
            if resp_code == 0:
                return None, "Network unreachable"
            elif resp_code == 1:
                return None, "Host unreachable"
        else:
            return None, f"Unexpected ICMP reply"
    except socket.timeout:
        return None, "Request timeout"
    except Exception as e:
        return None, f"Unexpected error {str(e)}"
    finally:
        icmp_socket.close()


def get_statistic_string(history):
    if len(history):
        data = np.array(history)
        return f"{data.min():.2f}/{data.mean():.2f}/{data.max():.2f}/{data.std():.2f} ms"
    else:
        return f"-/-/-/- ms"


if __name__ == "__main__":
    addresses = [('192.168.31.77', 0), ("google.com", 0), ("yahoo.co.jp", 0)]

    for addr in addresses:
        history = []
        print(f"PING {addr[0]}:")
        NUM = 10
        for icmp_seq in range(NUM):
            rtt, msg = my_ping(addr, icmp_seq)
            if rtt:
                history.append(rtt)
                print(
                    f"Reply from {addr[0]}: icmp_seq={icmp_seq} time={rtt:.2f} ms min/avg/max/stddev={get_statistic_string(history)}")
            else:
                print(f"{msg} for icmp_seq {icmp_seq}")
        print(f"--- {addr[0]} ping statistics ---")
        print("round-trip min/avg/max/stddev =", get_statistic_string(history))
        print(
            f"{NUM} packets transmitted, {len(history)} packets received, {(1 - len(history) / NUM) * 100:.2f}% packet loss")
