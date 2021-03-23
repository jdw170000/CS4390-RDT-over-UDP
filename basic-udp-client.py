import configparser
import socket

import rdt_headers
import send_packet

# read the server's port number and ip from the configuration file
config = configparser.ConfigParser()
config.read('udp.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send packets to server
for seq in range(10):
    while (True):
        message = f'This is packet {seq} of 9'
        print(f'Sending message: {message}')
        send_packet.send_message(sock, (server_ip, server_port), seq, message, corrupt_prob=.5)

        print(f'Awaiting ACK for sequence number {seq}')
        message_data, server_address = sock.recvfrom(1024)
        checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
        is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)

        print(
            f'Received response from server: message:{message}, sequence_number:{sequence_number}, is_valid:{is_valid}')

        if is_valid and message == b'ACK':  # messages are received as byte strings
            print(f'Received ACK for sequence number {seq}; moving to next packet')
            break
        else:
            if is_valid and message == b'NACK':  # messages are received as byte strings
                print(f'Received NACK for sequence number {seq}; retransmitting')
            else:
                print(f'Received invalid acknowledgement message for sequence number {seq}; retransmitting')
