import configparser
import socket

#read the server's port number and ip from the configuration file
config = configparser.ConfigParser()
config.read('udp.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

#create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send packets to server
for i in range(10):
    message = bytes(f'This is packet {i+1} of 10', 'utf-8')
    print(f'Sending message: {message}')
    sock.sendto(message, (server_ip, server_port))
