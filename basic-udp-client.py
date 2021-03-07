import configparser
import socket

import rdt_headers

#read the server's port number and ip from the configuration file
config = configparser.ConfigParser()
config.read('udp.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

#create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send packets to server
for seq in range(10):
    message = bytes(f'This is packet {seq} of 9', 'utf-8')
    header = rdt_headers.make_header(seq, message)
    packet = header + message
    print(f'Sending message: {message}')
    sock.sendto(packet, (server_ip, server_port))
