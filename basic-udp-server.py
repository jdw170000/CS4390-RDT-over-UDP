import configparser
import socket

#read the server's port number and ip address from the configuration file
config = configparser.ConfigParser()
config.read('udp.conf')
server_ip = config['server']['ip']
server_port = int(config['server']['port'])

#create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#bind socket to server-ip, server-port
sock.bind((server_ip, server_port))

#read data and print to terminal
while True:
    print('Waiting for client message...')
    message_data, client_address = sock.recvfrom(1024)
    print(f'Received message: {message_data}; from client: {client_address}')
