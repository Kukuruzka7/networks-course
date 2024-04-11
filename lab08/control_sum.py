def get_sum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        byte1 = data[i] if i < len(data) else 0
        byte2 = data[i + 1] if i + 1 < len(data) else 0
        num = (byte1 << 8) + byte2
        checksum += num
    checksum &= 0xffff
    return checksum


def get_control_sum(data: bytearray):
    return get_sum(data) ^ 0xffff


def check_control_sum(data: bytearray, control_sum):
    data_to_check = data + control_sum.to_bytes(2, byteorder='big')
    return get_sum(data_to_check) == 0xffff


def test_get_control_sum():
    assert get_control_sum(bytearray()) == 0xFFFF
    assert get_control_sum(bytearray([0xFF])) == 0x00FF
    assert get_control_sum(bytearray([0x12, 0x34, 0x56, 0x78, 0x9A])) == 0xFD53
    assert get_control_sum(bytearray([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC])) == 0xFC97


def test_check_control_sum():
    data1 = bytearray([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC])
    control_sum1 = get_control_sum(data1)
    assert check_control_sum(data1, control_sum1) == True

    data2 = bytearray([0x12, 0x34, 0x56, 0x78, 0x9A])
    control_sum2 = get_control_sum(data2)
    assert check_control_sum(data2, control_sum2) == False


if __name__ == "__main__":
    test_get_control_sum()
    test_check_control_sum()
    print("All tests passed!")
