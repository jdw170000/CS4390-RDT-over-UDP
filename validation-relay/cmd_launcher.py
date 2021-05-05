import os, sys
sys.path.insert(0, os.path.abspath(".."))

import argparse
import socket

# Create arg parser
import time

from rdt.rdt_client import RDT_Client
from rdt.rdt_server import RDT_Server

parser = argparse.ArgumentParser()

# Add args
parser.add_argument('-ws', '--window-size', required=True)
parser.add_argument('-ps', '--payload-size', required=False)
parser.add_argument('-cp', '--corrupt-prob', required=False)
parser.add_argument('-f', '--file', required=False)

parser.add_argument('-m', '--mode', required=True)  # client/server
parser.add_argument('-a', '--algo', required=True)  # GBN or SR
parser.add_argument('-ip', '--ip', required=True)
parser.add_argument('-p', '--port', required=True)

parser.add_argument('-d' , '--delay', required=True)

# Parse args
args = vars(parser.parse_args())
print(args)

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket

if (args['mode'] == 'server'):
    # Server mode
    print(f'Attempting to bind to {args["ip"]}:{args["port"]}')
    sock.bind((args['ip'], int(args['port'])))  # bind socket to server-ip, server-port

    rdt_server = RDT_Server(sock, args['algo'], timeout_value=1, window_size=int(args['window_size']))
    rdt_server.server.server.join()
    rdt_server.print_statistics()
elif (args['mode'] == 'client'):
    # Client mode
    rdt_client = RDT_Client(server_address=(args['ip'], int(args['port'])), mode=args['algo'], send_fail_delay=1,
                            max_payload_size=int(args['payload_size']), sock=sock, timeout_value=1,
                            window_size=int(args['window_size']), corrupt_probability=float(args['corrupt_prob']))
    start_time = time.perf_counter()
    rdt_client.send_file(args['file'][1:-1])
    rdt_client.done()
    # wait for the client to finish receiving acks
    rdt_client.client.receiver.join()
    end_time = time.perf_counter()
    rdt_client.client.statistics.elapsed = end_time - start_time
    rdt_client.print_statistics()
else:
    raise Exception(args['mode'] + ' is not a valid mode')
