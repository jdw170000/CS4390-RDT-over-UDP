import socket
import threading

from rdt.record_definitions import *
from rdt import rdt_headers, send_packet


class GBN_Server:
    sock = 0
    sequence_number_count = 11
    expected_sequence_number = 0
    current_ack = None
    server_timeout = 10
    statistics = None

    server = None

    def __init__(self, sock, server_timeout=10, window_size=10, initial_sequence_number=0, sequence_number_count=None):
        self.sock = sock
        self.server_timeout = server_timeout
        self.sequence_number_count = sequence_number_count if sequence_number_count is not None else window_size + 1
        self.expected_sequence_number = initial_sequence_number

        self.statistics = ServerStatistics(0, 0, 0)
        self.done = False

        self.server = threading.Thread(target=self.receiver_thread)
        self.server.start()

    def receiver_thread(self):
        while True:
            # receive message from server and parse it
            try:
                message_data, client_address = self.sock.recvfrom(1024)
                checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
                # validate the checksum
                is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)

                # if the packet is valid and in order, process it and update current ACK value
                if is_valid and sequence_number == self.expected_sequence_number:
                    self.statistics.numBytes += len(message)
                    print(f'Setting ACK ({sequence_number})')
                    self.current_ack = GBN_PacketDescriptor('ACK', self.expected_sequence_number)
                    self.expected_sequence_number = (self.expected_sequence_number + 1) % self.sequence_number_count

                    if message == b'DONE':
                        print('DONE received')
                        self.sock.settimeout(self.server_timeout)

                else:
                    if not is_valid:
                        self.statistics.numErrors += 1
                    else:
                        self.statistics.numOutOfSeq += 1

                # if we have an ack value, send it
                if self.current_ack is not None:
                    print(f'Sending ACK ({self.current_ack.sequence_number})')
                    send_packet.send_message(self.sock, client_address, self.current_ack.sequence_number,
                                             self.current_ack.message)

            except socket.timeout:
                print('Client is done and server_timeout has elapsed. Closing server...')
                break
