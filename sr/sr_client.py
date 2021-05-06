import configparser
import threading
import time

from rdt.record_definitions import *
from rdt import rdt_headers, send_packet

# # read the server's port number and ip from the configuration file
# config = configparser.ConfigParser()
# config.read('rdt.conf')
# server_ip = config['server']['ip']
# server_port = int(config['server']['port'])

# timeout_value = 5  # later this will be part of the config file
# window_size = 10  # later this will be part of the config file


class SR_Client:
    window_size = 10
    sequence_number_count = 20
    window_base = 0
    next_sequence_number = 0
    undelivered_list = []
    sock = 0
    server_address = ('127.0.0.1', 8080)
    internal_lock = threading.Lock()
    timeout_delay = 5
    corrupt_probability = 0
    done = False

    statistics = None
    receiver = None

    def __init__(self, sock, server_address, timeout_delay=5, window_size=10, initial_sequence_number=0,
                 sequence_number_count=None, corrupt_probability=0):
        self.sock = sock
        self.server_address = server_address
        self.window_size = window_size
        self.sequence_number_count = sequence_number_count if sequence_number_count is not None else window_size * 2
        self.window_base = next_sequence_number = initial_sequence_number
        self.timeout_delay = timeout_delay
        self.corrupt_probability = corrupt_probability

        self.internal_lock = threading.Lock()
        self.done = False

        self.statistics = ClientStatistics(0, 0, 0, 0, 0, None)

        self.receiver = threading.Thread(target=self.receiver_thread)
        self.receiver.start()

    def done_sending(self):
        while not self.send('DONE'):
            time.sleep(0.5)
        self.done = True

    def start_packet_timer(self, packet):
        packet.timer.cancel()
        packet.timer = threading.Timer(self.timeout_delay, self.retransmit_packet(packet))
        packet.timer.start()

    # factroy function to make packet retransmission functions for use during timeout
    def retransmit_packet(self, packet):
        def retransmit():
            self.internal_lock.acquire()

            print(f'Retransmitting unacked packet {packet.sequence_number}')
            self.statistics.numRetransmits += 1
            self.statistics.numTOevents += 1

            # retransmit the packet and reset the timer
            send_packet.send_message(self.sock, self.server_address, packet.sequence_number, packet.message)
            self.start_packet_timer(packet)

            self.internal_lock.release()

        return retransmit

    def send(self, message):
        # you are not allowed to send new packet after saying you are done
        if self.done:
            raise RuntimeError('Cannot send messages from client after done')

        # if the next sequence number is not in the range of valid sequence numbers, we can't send the packet
        if self.next_sequence_number not in [x % self.sequence_number_count for x in
                                             range(self.window_base, self.window_base + self.window_size)]:
            print(
                f'sequence number {self.next_sequence_number} is not in the window starting at {self.window_base} with size {self.window_size} modulo {self.sequence_number_count}')
            return False

        self.internal_lock.acquire()

        # send the message and add it to the list of undelivered packets
        packet = SR_PacketDescriptor(message, self.next_sequence_number, False, None)
        packet.timer = threading.Timer(self.timeout_delay, self.retransmit_packet(packet));

        print(f'Sending packet: ({packet.message}, {packet.sequence_number})')
        self.statistics.numTransmits += 1
        self.statistics.numBytes += len(message)  # only count the payload bytes in the bytes sent

        corrupted = send_packet.send_message(self.sock, self.server_address, packet.sequence_number, packet.message,
                                             corrupt_prob=self.corrupt_probability)
        if corrupted:
            self.statistics.numCorrupts += 1

        self.undelivered_list.append(packet)
        self.start_packet_timer(packet)

        # increment sequence number
        self.next_sequence_number = (self.next_sequence_number + 1) % self.sequence_number_count

        self.internal_lock.release()

        return True

    def mark_as_acked(self, packet):
        packet.acked = True
        packet.timer.cancel()

        # deliver all continuous acked packets at the bottom of the window
        while self.undelivered_list and self.undelivered_list[0].acked:
            delivered_packet = self.undelivered_list.pop(0)
            delivered_packet.timer.cancel()
            print(f'Packet {delivered_packet.sequence_number} has been delivered')
            self.window_base = (delivered_packet.sequence_number + 1) % self.sequence_number_count

    def receiver_thread(self):
        # count consecutive server timeouts
        timeout_count = 0

        # repeat until we have received ack for all messages and the client is done sending messages
        while self.undelivered_list or not self.done:
            # receive message from server and parse it
            try:
                self.sock.settimeout(self.timeout_delay)
                message_data, server_address = self.sock.recvfrom(1024)
                timeout_count = 0
                checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
                # validate the checksum
                is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)
                # if the ACK is valid and in the window, process it
                if is_valid and sequence_number in [s % self.sequence_number_count for s in range(self.window_base, self.window_base + self.window_size)]:
                    self.internal_lock.acquire()

                    try:
                        # shift the window to the acked sequence number, removing acked packets from the unacked list
                        acked_packet = next(p for p in self.undelivered_list if p.sequence_number == sequence_number)
                        self.mark_as_acked(acked_packet)

                        print(f'Received ACK({sequence_number}), packet marked as acked')
                    except StopIteration:
                        print(f'Received ACK({sequence_number}), but that packet was not found in the undelivered list')
                    
                    self.internal_lock.release()
            except:
                if self.undelivered_list:
                    timeout_count += 1
                print("Timed out waiting for reply from server")
                if self.done and timeout_count > 10:
                    for p in self.undelivered_list: p.timer.cancel()
                    return

