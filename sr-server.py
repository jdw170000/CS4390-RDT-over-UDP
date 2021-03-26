import configparser
import socket
import threading
import bisect
from collections import namedtuple

import rdt_headers
import send_packet

# read the server's port number and ip address from the configuration file
config = configparser.ConfigParser()
config.read('udp.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

window_size = 10  # later this will be part of the config file
timeout_value = 2 * 5  # later this will be part of the config file

PacketDescriptor = namedtuple('PacketDescriptor', 'message sequence_number')


class SR_Server:
    sock = 0
    window_base = 0
    window_size = 10
    sequence_number_count = 20
    server_timeout = 10

    delivery_buffer = []

    def __init__(self, sock, server_timeout=10, window_size=10, initial_sequence_number=0, sequence_number_count=None):
        self.sock = sock
        self.window_base = initial_sequence_number
        self.window_size = window_size
        self.server_timeout = server_timeout
        self.sequence_number_count = sequence_number_count if sequence_number_count is not None else window_size*2

        self.done = False

    def start_server(self):
        server = threading.Thread(target=self.receiver_thread)
        server.start()

    #do some processing on the packet
    def deliver(self, packet):
        self.window_base = (self.window_base + 1) % self.sequence_number_count
        print(f'Delivered packet {packet.sequence_number}')

    #deliver all in order packets received
    def attempt_to_deliver_packets(self):
        print(f'Attempting to deliver packets: window base = {self.window_base}, delivery_buffer = {str([p.sequence_number for p in self.delivery_buffer])}')
        while self.delivery_buffer and self.delivery_buffer[0].sequence_number == self.window_base:
            self.deliver(self.delivery_buffer.pop(0))

    def receiver_thread(self):
        while True:
            # receive message from server and parse it
            try:
                message_data, client_address = self.sock.recvfrom(1024)
                checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
                # validate the checksum
                is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)

                # if the packet is valid and in the window, process it
                if is_valid and sequence_number in [s % self.sequence_number_count for s in range(self.window_base, self.window_base + self.window_size)]: 
                    #send the ack and attempt to deliver the packet
                    ack = PacketDescriptor('ACK', sequence_number)
                    print(f'Sending ACK ({ack.sequence_number})')
                    send_packet.send_message(self.sock, client_address, ack.sequence_number, ack.message)

                    packet = PacketDescriptor(message, sequence_number)

                    # if the packet is in order, deliver it and attempt to deliver more, otherwise buffer it
                    if(packet.sequence_number == self.window_base):
                        self.deliver(packet)
                        self.attempt_to_deliver_packets()
                    else:
                        bisect.insort(self.delivery_buffer, packet)

                    if message == b'DONE':
                        print('DONE received')
                        self.sock.settimeout(self.server_timeout)

            except socket.timeout:
                print('Client is done and server_timeout has elapsed. Closing server...')
                break


# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind socket to server-ip, server-port
sock.bind((server_ip, server_port))

server = SR_Server(sock, window_size=window_size, server_timeout=timeout_value)
server.start_server()
