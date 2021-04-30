import random
from rdt import rdt_headers


def send_ack(sock, address, sequence_number):
    send_message(sock, address, sequence_number, 'ACK')


def send_nack(sock, address, sequence_number):
    send_message(sock, address, sequence_number, 'NACK')


def send_message(sock, address, sequence_number, message, corrupt_prob=0):
    # encode packet
    bytes_message = bytes(message, 'utf-8')
    header = rdt_headers.make_header(sequence_number, bytes_message)
    packet = bytearray(header + bytes_message)

    corrupt = False

    # flip a random bit depending on corrupt_prob
    if (random.random() < corrupt_prob):
        bit_to_invert = random.randrange(0, len(packet) * 8)  # choose bit to invert at random
        byte_to_invert = bit_to_invert // 8  # determine what byte bit is located in
        bitmasks = [0b10000000, 0b01000000, 0b00100000, 0b00010000, 0b00001000, 0b00000100, 0b00000010, 0b00000001]  # bitmasks for flipping each bit in byte

        packet[byte_to_invert] = packet[byte_to_invert] ^ bitmasks[bit_to_invert % 8]
        corrupt = True

    # send packet
    sock.sendto(bytes(packet), address)

    return corrupt
