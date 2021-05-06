import threading
import time
from rdt.record_definitions import *
from rdt import rdt_headers, send_packet


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
    corrupt_probability = 0

    timeout_timer = None
    done = False

    statistics = None
    receiver = None

    def __init__(self, sock, server_address, timeout_delay=5, window_size=10, initial_sequence_number=0,
                 sequence_number_count=None, corrupt_probability=0):
        self.sock = sock
        self.server_address = server_address
        self.window_size = window_size
        self.sequence_number_count = sequence_number_count if sequence_number_count is not None else window_size + 1
        self.window_base = next_sequence_number = initial_sequence_number
        self.timeout_delay = timeout_delay
        self.corrupt_probability = corrupt_probability

        self.timeout_timer = threading.Timer(timeout_delay, self.retransmit_unacked_messages)

        self.internal_lock = threading.Lock()
        self.done = False

        self.statistics = ClientStatistics(0, 0, 0, 0, 0, None)

        self.receiver = threading.Thread(target=self.receiver_thread)
        self.receiver.start()

    def done_sending(self):
        while not self.send('DONE'): 
            time.sleep(0.5)
        self.done = True

    def start_timer(self):
        self.timeout_timer.cancel()
        self.timeout_timer = threading.Timer(self.timeout_delay, self.retransmit_unacked_messages)
        self.timeout_timer.start()

    def stop_timer(self):
        self.timeout_timer.cancel()

    def retransmit_unacked_messages(self):
        self.internal_lock.acquire()

        self.statistics.numTOevents += 1
        self.statistics.numRetransmits += len(self.unacked_list)

        self.start_timer()

        print('Retransmitting unacked packets')
        for packet in self.unacked_list:
            corrupted = send_packet.send_message(self.sock, self.server_address, packet.sequence_number, packet.message)
            print(f'Retransmitting packet {packet.sequence_number} (corrputed? {corrupted})...')

        self.internal_lock.release()

    def send(self, message):
        # you are not allowed to send new packet after saying you are done
        if self.done:
            raise RuntimeError('Cannot send messages from client after done')

        # if the next sequence number is not in the range of valid sequence numbers, we can't send the packet
        if self.next_sequence_number not in [x % self.sequence_number_count for x in
                                             range(self.window_base, self.window_base + self.window_size)]:
            return False

        self.internal_lock.acquire()

        # send the message and add it to the list of unacked packets
        packet = GBN_PacketDescriptor(message, self.next_sequence_number)

        print(f'Sending packet: ({packet.message}, {packet.sequence_number})')
        self.statistics.numTransmits += 1
        self.statistics.numBytes += len(message)

        corrupt = send_packet.send_message(self.sock, self.server_address, packet.sequence_number, packet.message,
                                           corrupt_prob=self.corrupt_probability)
        if corrupt:
            self.statistics.numCorrupts += 1

        self.unacked_list.append(packet)

        # if this is the first packet of the window, start the timeout timer
        if self.window_base == self.next_sequence_number:
            self.start_timer()

        # increment sequence number
        self.next_sequence_number = (self.next_sequence_number + 1) % self.sequence_number_count

        self.internal_lock.release()

        return True

    def send_message_set(self, message_set):
        for m in message_set:
            self.send(m)

    def receiver_thread(self):
        # count consecutive timeouts
        timeout_count = 0

        # repeat until we have received ack for all messages and the client is done sending messages
        while self.unacked_list or not self.done:
            # receive message from server and parse it
            try:
                self.sock.settimeout(self.timeout_delay)
                message_data, server_address = self.sock.recvfrom(1024)
                timeout_count = 0
                checksum, sequence_number, message = rdt_headers.parse_rdt_packet(message_data)
                # validate the checksum
                is_valid = rdt_headers.is_valid_checksum(checksum, sequence_number, message)
                # if the ACK is valid, process it
                if is_valid:
                    self.internal_lock.acquire()

                    # shift the window to the acked sequence number, removing acked packets from the unacked list
                    if(any([x.sequence_number == sequence_number for x in self.unacked_list])):
                        shift_amount = (sequence_number + 1 - self.window_base) % self.sequence_number_count
                        print(f'Unacked list before shift: {", ".join([str(x.sequence_number) for x in self.unacked_list])}; window_base = {self.window_base}')
                        self.unacked_list = self.unacked_list[shift_amount:]
                        self.window_base = (sequence_number + 1) % self.sequence_number_count
                        print(f'Unacked list after shift: {", ".join([str(x.sequence_number) for x in self.unacked_list])}; window_base = {self.window_base}')

                        print(f'Received ACK({sequence_number}), window_base set to {self.window_base}')
                        
                        # if we have no more unacked packets, stop the timer
                        # otherwise, start the timer
                        if self.window_base == self.next_sequence_number:
                            self.stop_timer()
                        else:
                            self.start_timer()
                    
                    self.internal_lock.release()
            except:
                if self.unacked_list:
                    timeout_count += 1
                print(f'Timed out waiting for reply from server; timeout_count = {timeout_count}')
                if self.done and timeout_count > 10:
                    self.timer.cancel()
                    return
            
