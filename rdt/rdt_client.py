import time

from gbn.gbn_client import GBN_Client
from sr.sr_client import SR_Client


class RDT_Client:
    client = None

    MAX_PAYLOAD_SIZE = None
    send_fail_delay = None

    server_address = None

    def __init__(self, server_address, mode='GBN', send_fail_delay=1, max_payload_size=100, sock=None, timeout_value=5,
                 window_size=10, initial_sequence_number=0, sequence_number_count=None, corrupt_probability=0):

        self.MAX_PAYLOAD_SIZE = max_payload_size
        self.send_fail_delay = send_fail_delay

        if mode == 'GBN':
            self.client = GBN_Client(sock=sock, server_address=server_address, timeout_delay=timeout_value,
                                     window_size=window_size, initial_sequence_number=initial_sequence_number,
                                     sequence_number_count=sequence_number_count,
                                     corrupt_probability=corrupt_probability)
        elif mode == 'SR':
            self.client = SR_Client(sock=sock, server_address=server_address, timeout_delay=timeout_value,
                                    window_size=window_size, initial_sequence_number=initial_sequence_number,
                                    sequence_number_count=sequence_number_count,
                                    corrupt_probability=corrupt_probability)
        else:
            raise ValueError('mode must be GBN or SR')

    def print_statistics(self):
        stats = self.client.statistics
        print('\n'.join([
            'SENDER STATISTICS',
            f'numTransmits = {stats.numTransmits}',
            f'umRetransmits = {stats.numRetransmits}',
            f'numTOevents = {stats.numTOevents}',
            f'numBytes = {stats.numBytes}',
            f'numCorrupts = {stats.numCorrupts}',
            f'elapsed = {stats.elapsed}'
        ]))

    # try to send all the messages; if you can't send a message, wait send_fail_delay seconds and try again
    def send_message_set(self, message_set):
        for m in message_set:
            if len(m) > self.MAX_PAYLOAD_SIZE:
                raise ValueError(f'message payloads cannot be larger than {self.MAX_PAYLOAD_SIZE} Bytes')
            while not self.client.send(m):
                time.sleep(self.send_fail_delay)

    def send_message(self, message):
        # split the message into payload sized chunks and send them
        self.send_message_set(
            [message[0 + i:self.MAX_PAYLOAD_SIZE + i] for i in range(0, len(message), self.MAX_PAYLOAD_SIZE)])

    def send_file(self, filename):
        # create a message generator for the file that reads MAX_PAYLOAD_SIZE bytes at a time
        def message_generator(filename):
            with open(filename, 'rb') as infile:
                message = infile.read(self.MAX_PAYLOAD_SIZE)
                while message:
                    yield str(message, 'utf-8')
                    message = infile.read(self.MAX_PAYLOAD_SIZE)

        # send the message set for the file
        self.send_message_set(message_generator(filename))

    def done(self):
        self.client.done_sending()
