import argparse
import socket
import struct
import time


def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + (data[i + 1])
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF
    return checksum


def one_request(addr, icmp_seq, ttl):
    icmp = socket.getprotobyname("icmp")
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    icmp_socket.settimeout(2)
    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    icmp_type = 8  # Тип ICMP-сообщения (эхо-запрос)
    icmp_code = 0  # Код ICMP-сообщения
    icmp_id = 1000  # Идентификатор пакета
    icmp_checksum = calculate_checksum(struct.pack('!BBHHH', icmp_type, icmp_code, 0, icmp_id, icmp_seq))
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
    try:
        start_time = time.time()
        icmp_socket.sendto(icmp_header, (addr, 0))
        reply, curr_addr = icmp_socket.recvfrom(1024)
        end_time = time.time()
        rtt = (end_time - start_time) * 1000
        resp_type, resp_code = struct.unpack('!BB', reply[20:22])
        if resp_type == 0 and resp_code == 0:
            return rtt, curr_addr[0], "Destination reached"
        if resp_type == 3:
            if resp_code == 0:
                return None, curr_addr[0], "Network unreachable"
            elif resp_code == 1:
                return None, curr_addr[0], "Host unreachable"
        if resp_type == 11:
            if resp_code == 0:
                return rtt, curr_addr[0], "Network unreachable"
            elif resp_code == 1:
                return None, curr_addr[0], "Unexpected ICMP reply"
        else:
            return None, curr_addr[0], f"Unexpected ICMP reply"
    except socket.timeout:
        return None, None, "Request timeout"
    except Exception as e:
        return None, None, f"Unexpected error {str(e)}"
    finally:
        icmp_socket.close()


def print_traceroute_result(ttl, hostname=None, ip=None, rtts=None):
    # Формат строки с фиксированной шириной для каждого столбца
    if ip is None:
        print(f"{ttl:<8} {'*':<40}")
    else:
        if hostname is None:
            print(f"{ttl:<8} {'*':<40} {ip:<20} {rtts[0]:<8} {rtts[1]:<8} {rtts[2]:<8} ms")
        else:
            print(f"{ttl:<8} {hostname:<40} {ip:<20} {rtts[0]:<8} {rtts[1]:<8} {rtts[2]:<8} ms")


def traceroute(dest_name, max_hops=30, packets_per_hop=3):
    dest_addr = socket.gethostbyname(dest_name)
    print(f"Traceroute to {dest_name} ({dest_addr}), {max_hops} hops max")
    for ttl in range(1, max_hops + 1):
        history = []
        addr = None
        for try_number in range(packets_per_hop):
            rtt, curr_addr, msg = one_request(dest_addr, (ttl - 1) * packets_per_hop + try_number, ttl)
            if (addr is None) and (curr_addr is not None):
                addr = curr_addr
                history.append(rtt)
            elif addr is not None:
                if addr != curr_addr:
                    history.append(None)
                else:
                    history.append(rtt)
            else:
                history.append(rtt)
        if addr is None:
            print_traceroute_result(ttl, None, addr, None)
        if addr is not None:
            host_name = None
            try:
                host_name = socket.gethostbyaddr(addr)[0]
            except socket.herror as e:
                pass
            for _ in range(packets_per_hop - len(history)):
                history.append(None)
            for i in range(len(history)):
                if history[i] is None:
                    history[i] = "*"
                else:
                    history[i] = round(history[i], 2)
            print_traceroute_result(ttl, host_name, addr, history)

        if addr == dest_addr:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', default="google.com")
    parser.add_argument('-max_hops', type=int, default=30)
    parser.add_argument('-packets_per_hop', type=int, default=3)
    args = parser.parse_args()
    traceroute(args.host, max_hops=args.max_hops, packets_per_hop=args.packets_per_hop)
