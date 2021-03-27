import socket
import threading

from record_definitions import *
import rdt_headers
import send_packet

class SR_Server:
    sock = 0
    window_base = 0
    window_size = 10
    sequence_number_count = 20
    server_timeout = 10

    server = None

    statistics = None
    delivery_buffer = []

    def __init__(self, sock, server_timeout=10, window_size=10, initial_sequence_number=0, sequence_number_count=None):
        self.sock = sock
        self.window_base = initial_sequence_number
        self.window_size = window_size
        self.server_timeout = server_timeout
        self.sequence_number_count = sequence_number_count if sequence_number_count is not None else window_size*2

        self.done = False
        
        self.statistics = ServerStatistics(0,0,'N/A')

        self.server = threading.Thread(target=self.receiver_thread)
        self.server.start()

    #do some processing on the packet
    def deliver(self, packet):
        self.window_base = (self.window_base + 1) % self.sequence_number_count
        print(f'Delivered packet {packet.sequence_number}')
        self.statistics.numBytes += len(packet.message)
        

    #deliver all in order packets received
    def attempt_to_deliver_packets(self):
        print(f'Attempting to deliver packets: window base = {self.window_base}, delivery_buffer = {str([p.sequence_number for p in self.delivery_buffer])}')
        while self.delivery_buffer and self.delivery_buffer[0].sequence_number == self.window_base:
            self.deliver(self.delivery_buffer.pop(0))
    
    def buffer_packet(self, packet):
        #insert the packet in sorted order by sequence number to the buffer list
        for index, buffered_packet in enumerate(self.delivery_buffer):
            if buffered_packet.sequence_number > packet.sequence_number:
                self.delivery_buffer.insert(index, packet)
                return
        #if this packet is the greatest element in the list, append it instead
        self.delivery_buffer.append(packet)

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
                    ack = GBN_PacketDescriptor('ACK', sequence_number)
                    print(f'Sending ACK ({ack.sequence_number})')
                    send_packet.send_message(self.sock, client_address, ack.sequence_number, ack.message)

                    packet = GBN_PacketDescriptor(message, sequence_number)

                    # if the packet is in order, deliver it and attempt to deliver more, otherwise buffer it
                    if(packet.sequence_number == self.window_base):
                        self.deliver(packet)
                        self.attempt_to_deliver_packets()
                    else:
                        self.buffer_packet(packet)

                    if message == b'DONE':
                        print('DONE received')
                        self.sock.settimeout(self.server_timeout)
                else:
                    if not is_valid:
                        self.statistics.numErrors += 1

            except socket.timeout:
                print('Client is done and server_timeout has elapsed. Closing server...')
                break
