import configparser
import socket
import threading

from rdt_server import RDT_Server


# read the server's port number and ip address from the configuration file
config = configparser.ConfigParser()
config.read('rdt.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

window_size = int(config['global']['window_size']) 
timeout_value = int(config['server']['timeout'])

mode = config['global']['mode']

###########################################################################################

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind socket to server-ip, server-port
sock.bind((server_ip, server_port))

rdt_server = RDT_Server(sock, mode, timeout_value = timeout_value, window_size = window_size)

rdt_server.server.server.join()

rdt_server.print_statistics()

