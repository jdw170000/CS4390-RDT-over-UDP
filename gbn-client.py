import configparser
import sys
import socket
import threading
import queue
from collections import namedtuple

import rdt_headers
import send_packet

# read the server's port number and ip from the configuration file
config = configparser.ConfigParser()
config.read('udp.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

timeout_value = 5  # later this will be part of the config file
window_size = 10  # later this will be part of the config file

PacketDescriptor = namedtuple('PacketDescriptor', 'message sequence_number')


class GBN_Client:
    window_size = 10
    sequence_number_count = 11
    window_base = 0
    next_sequence_number = 0
    unacked_list = []
    sock = 0
    server_address = ('127.0.0.1', 8080)
    internal_lock = threading.Lock()
    timeout_delay = 5
    timeout_timer = None
    done = False

    receiver = None

    def __init__(self, sock, server_address, timeout_delay=5, window_size=10, initial_sequence_number=0,
                 sequence_number_count=None):
        self.sock = sock
        self.server_address = server_address
        self.window_size = window_size
        self.sequence_number_count = sequence_number_count if sequence_number_count is not None else window_size + 1
        self.window_base = next_sequence_number = initial_sequence_number
        self.timeout_delay = timeout_delay
        self.timeout_timer = threading.Timer(timeout_delay, self.retransmit_unacked_messages)

        self.internal_lock = threading.Lock()
        self.done = False

        self.receiver = threading.Thread(target=self.receiver_thread)
        self.receiver.start()

    def done_sending(self):
        self.send('DONE')
        self.done = True

    def start_timer(self):
        self.timeout_timer.cancel()
        self.timeout_timer = threading.Timer(self.timeout_delay, self.retransmit_unacked_messages)
        self.timeout_timer.start()

    def stop_timer(self):
        self.timeout_timer.cancel()

    def retransmit_unacked_messages(self):
        self.internal_lock.acquire()

        self.start_timer()

        print('Retransmitting unacked packets')
        for packet in self.unacked_list:
            send_packet.send_message(self.sock, self.server_address, packet.sequence_number, packet.message)
        self.internal_lock.release()

    def send(self, message):
        # you are not allowed to send new packet after saying you are done
        if self.done:
            raise RuntimeError('Cannot send messages from client after done')

        #if the next sequence number is not in the range of valid sequence numbers, we can't send the packet
        if self.next_sequence_number not in [x % sequence_number_count for x in range(self.window_base, self.window_base + self.window_size)]:
            return False
        
        self.internal_lock.acquire()

        # send the message and add it to the list of unacked packets
        packet = PacketDescriptor(message, self.next_sequence_number)
        print(f'Sending packet: ({packet.message}, {packet.sequence_number})')
        send_packet.send_message(self.sock, self.server_address, packet.sequence_number, packet.message)
        self.unacked_list.append(packet)

        # if this is the first packet of the window, start the timeout timer
        if self.window_base == self.next_sequence_number:
            self.start_timer()

        # increment sequence number
        self.next_sequence_number = (self.next_sequence_number + 1) % self.sequence_number_count

        self.internal_lock.release()

    def send_message_set(self, message_set):
        for m in message_set:
            self.send(m)

    def receiver_thread(self):
        # repeat until we have received ack for all messages and the client is done sending messages
        while self.unacked_list or not self.done:
            # receive message from server and parse it
            message_data, server_address = sock.recvfrom(1024)
            checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
            # validate the checksum
            is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)
            # if the ACK is valid, process it
            if is_valid:
                self.internal_lock.acquire()

                # shift the window to the acked sequence number, removing acked packets from the unacked list
                shift_amount = (sequence_number + 1 - self.window_base) % self.sequence_number_count
                self.unacked_list = self.unacked_list[shift_amount:]
                self.window_base = (sequence_number + 1) % self.sequence_number_count

                print(f'Received ACK({sequence_number}), window_base set to {self.window_base}')

                # if we have no more unacked packets, stop the timer
                # otherwise, start the timer
                if self.window_base == self.next_sequence_number:
                    self.stop_timer()
                else:
                    self.start_timer()

            self.internal_lock.release()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (server_ip, server_port)

client = GBN_Client(sock, server_address, timeout_value, window_size)


def message_generator(n=10):
    for i in range(n):
        yield f'This is packet {i} of {n}'


client.send_message_set(message_generator(n=10))
client.done_sending()
