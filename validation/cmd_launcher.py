import argparse
import socket

# Create arg parser
import time

from rdt.rdt_server import RDT_Server
from rdt.rdt_client import RDT_Client

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

# Parse args
args = vars(parser.parse_args())

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
sock.bind((args['ip'], args['port']))  # bind socket to server-ip, server-port

if (args['mode'] == 'server'):
    # Server mode
    server = RDT_Server(sock, args['algo'], timeout_value=10, window_size=args['window-size'])
    server.server.server.join()
    server.print_statistics()
elif (args['mode'] == 'client'):
    # Client mode
    client = RDT_Client(server_address=args['ip'], mode=args['algo'], send_fail_delay=1,
                        max_payload_size=args['corrupt-prob'], sock=sock, timeout_value=5,
                        window_size=args['window-size'], corrupt_probability=args['corrupt-prob'])
    start_time = time.perf_counter()
    client.send_file(args['file'])
    client.done()
    # wait for the client to finish receiving acks
    client.client.receiver.join()
    end_time = time.perf_counter()
    client.client.statistics.elapsed = end_time - start_time
    client.print_statistics()
else:
    raise Exception(args['mode'] + ' is not a valid mode')
