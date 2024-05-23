from crc import calculate_crc, introduce_error


def test_main(packet_size: int = 5, num_errors: int = 1):
    text = "Hello, this is a test message to demonstrate CRC checking."
    bytes_data = text.encode()
    packets = [bytes_data[i:i + packet_size] for i in range(0, len(bytes_data), packet_size)]

    for i, packet in enumerate(packets):
        crc = calculate_crc(packet)
        encoded_packet = packet + crc.to_bytes(4, byteorder='big')

        if i % 2 == 0:
            packet_with_error = introduce_error(encoded_packet, num_errors)
            data_with_error = packet_with_error[:-4]
            assert calculate_crc(
                packet_with_error) != crc, f"CRC mismatch not detected. Data: {packet}. " \
                                           f"Data with error: {data_with_error}"


def test_crc_with_error():
    """
    Test CRC calculation and checking with introduced errors.
    """
    text = "Hello, World!"
    bytes_data = text.encode()
    packets = [bytes_data[i:i + 5] for i in range(0, len(bytes_data), 5)]

    for packet in packets:
        crc = calculate_crc(packet)
        packet_with_error = introduce_error(packet, 1)
        assert crc != calculate_crc(packet_with_error), "Failed to detect error in packet"


if __name__ == "__main__":
    test_crc_with_error()
    test_main()
    print("All tests passed.")
