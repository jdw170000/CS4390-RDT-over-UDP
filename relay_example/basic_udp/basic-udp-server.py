import configparser
import socket

# for testing purposes only
import random

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from rdt import rdt_headers, send_packet

# read the server's port number and ip address from the configuration file
config = configparser.ConfigParser()
config.read('relay.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind socket to server-ip, server-port
sock.bind((server_ip, server_port))

# read data and print to terminal
while True:
    print('Waiting for client message...')
    message_data, client_address = sock.recvfrom(1024)
    checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
    is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)

    print(f'Received packet: {message_data}; from client: {client_address}')
    print(f'Checksum ({checksum}) is valid? {is_valid}. Sequence number = {sequence_number}. Message = "{message}"')

    if is_valid and random.randint(1, 2) == 1:  # for testing purposes, send NACK half the time
        print(f'Sent ACK for sequence number {sequence_number}')
        send_packet.send_ack(sock, client_address, sequence_number)
    else:
        print(f'Sent NACK for sequence number {sequence_number}')
        send_packet.send_nack(sock, client_address, sequence_number)
