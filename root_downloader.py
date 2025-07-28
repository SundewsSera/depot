import hashlib
import base64

def parse_encoded_data(data: str):
    _, b64_data = data.split(":", 1)

    decoded = base64.b64decode(b64_data)

    size = decoded[0]

    checksum_bytes = decoded[1:9]
    checksum = int.from_bytes(checksum_bytes, byteorder='big', signed=True)

    return size, checksum

def calc_hname(checksum, size, name):
    name = name.encode("utf8")
    a = bytearray(16)

    for i in range(8):
        a[i] = (checksum >> ((7 - i) * 8)) & 0xFF

    for i in range(8):
        a[i+8] = (size >> ((7 - i) * 8)) & 0xFF

    data = a + name
    digest = hashlib.sha1(data).digest()
    return base64.b32encode(digest).decode('utf8')

version = "10016900:Td5E/sblqx6G"
size, checksum = parse_encoded_data(version)

print(calc_hname(checksum, size, 'root'))
