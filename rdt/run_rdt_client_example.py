import configparser
import socket
import threading
import time

from rdt_client import RDT_Client

# read the server's port number and ip from the configuration file
config = configparser.ConfigParser()
config.read('rdt.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

server_address = (server_ip, server_port)

mode = config['global']['mode']
timeout_value = int(config['client']['timeout'])
window_size = int(config['global']['window_size'])
send_fail_delay = int(config['client']['send_fail_delay'])

max_payload_size = int(config['client']['max_payload_size'])
corrupt_probability = float(config['client']['corrupt_probability'])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#####################################################################

def test_file(filename, rdt_client):
    start_time = time.perf_counter()

    rdt_client.send_file('myfile.txt')
    rdt_client.done()

    # wait for the client to finish receiving acks
    rdt_client.client.receiver.join()

    end_time = time.perf_counter()

    rdt_client.client.statistics.elapsed = end_time - start_time

    rdt_client.print_statistics()


#####################################################################

rdt_client = RDT_Client(server_address=server_address, mode=mode, send_fail_delay=send_fail_delay,
                        max_payload_size=max_payload_size, sock=sock, timeout_value=timeout_value,
                        window_size=window_size, corrupt_probability=corrupt_probability)

test_file('myfile.txt', rdt_client)
