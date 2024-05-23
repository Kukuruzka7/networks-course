import random


# crc32
def calculate_crc(data: bytes) -> int:
    crc = 0xFFFFFFFF
    polynomial = 0xEDB88320

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1

    return crc ^ 0xFFFFFFFF


def introduce_error(data: bytes, num_errors: int = 1) -> bytes:
    data_list = list(data)
    data_len = len(data_list)
    for _ in range(num_errors):
        byte_index = random.randint(0, data_len - 1)
        bit_index = random.randint(0, 7)
        data_list[byte_index] ^= 1 << bit_index
    return bytes(data_list)


def process_text(text: str, packet_size: int = 5):
    bytes_data = text.encode()
    packets = [bytes_data[i:i + packet_size] for i in range(0, len(bytes_data), packet_size)]

    for i, packet in enumerate(packets):
        crc = calculate_crc(packet)
        encoded_packet = packet + crc.to_bytes(4, byteorder='big')
        print(f"Packet {i + 1} - Data: {packet}, Encoded: {encoded_packet}, CRC: {crc:08X}")


if __name__ == "__main__":
    input_text = "Hello, this is a test message to demonstrate CRC checking."
    process_text(input_text)
