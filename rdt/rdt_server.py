import os, sys
sys.path.insert(0, os.path.abspath(".."))

from sr.sr_server import SR_Server
from gbn.gbn_server import GBN_Server


class RDT_Server:
    server = None

    def __init__(self, sock, mode='GBN', timeout_value=10, window_size=10, initial_sequence_number=0,
                 sequence_number_count=None):
        if mode == 'GBN':
            self.server = GBN_Server(sock=sock, server_timeout=timeout_value, window_size=window_size,
                                     initial_sequence_number=initial_sequence_number,
                                     sequence_number_count=sequence_number_count)
        elif mode == 'SR':
            self.server = SR_Server(sock=sock, server_timeout=timeout_value, window_size=window_size,
                                    initial_sequence_number=initial_sequence_number,
                                    sequence_number_count=sequence_number_count)

    def print_statistics(self):
        stats = self.server.statistics
        print('\n'.join([
            'RECEIVER STATISTICS',
            f'numBytes = {stats.numBytes}',
            f'numErrors = {stats.numErrors}',
            f'numOutOfSeq = {stats.numOutOfSeq}'
        ]))
