import configparser
import socket
import threading
from collections import namedtuple

import rdt_headers
import send_packet

#read the server's port number and ip address from the configuration file
config = configparser.ConfigParser()
config.read('udp.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])


window_size = 10 #later this will be part of the config file

PacketDescriptor = namedtuple('PacketDescriptor', 'message sequence_number')

class GBN_Server:
    sock = 0
    window_size = 10
    sequence_number_count = 11
    expected_sequence_number = 0
    current_ack = None
    server_timeout = 10

    def __init__(self, sock, server_timeout=10, window_size=10, initial_sequence_number=0, sequence_number_count = None):
        self.sock = sock
        self.window_size = window_size
        self.server_timeout = server_timeout
        self.sequence_number_count = sequence_number_count if sequence_number_count is not None else window_size + 1
        self.expected_sequence_number = initial_sequence_number

        self.done = False

    def start_server(self):
        server = threading.Thread(target=self.receiver_thread)
        server.start()

    def receiver_thread(self):
        while True:
            #receive message from server and parse it
            try:
                message_data, client_address = self.sock.recvfrom(1024)
                checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
                #validate the checksum
                is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)

                #if the packet is valid and in order, process it and update current ACK value
                if is_valid and sequence_number == self.expected_sequence_number:
                    print(f'Setting ACK ({sequence_number})')
                    self.current_ack = PacketDescriptor('ACK', self.expected_sequence_number)
                    self.expected_sequence_number = (self.expected_sequence_number + 1) % self.sequence_number_count

                    if message == b'DONE':
                        print('DONE received')
                        self.sock.settimeout(self.server_timeout)

                #if we have an ack value, send it
                if self.current_ack is not None:
                    print(f'Sending ACK ({self.current_ack.sequence_number})')
                    send_packet.send_message(self.sock, client_address, self.current_ack.sequence_number, self.current_ack.message)

            except socket.timeout:
                print('Client is done and server_timeout has elapsed. Closing server...')
                break

#create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#bind socket to server-ip, server-port
sock.bind((server_ip, server_port))

server = GBN_Server(sock, window_size=window_size, server_timeout=1)
server.start_server()
