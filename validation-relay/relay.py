import socket
from threading import Thread
import random
from time import sleep


def forward(sock, packet, destination_address, drop_rate=0.0, delay=0.0):
    # delay for the specified number of seconds
    sleep(delay)
    # drop packets with probability drop_rate
    if drop_rate < random.random():
        # forward the packet
        sock.sendto(bytes(packet), destination_address)


# begin listening for packets to forward
def begin(listener_address, server_address, drop_rate=0.0, delay=0.0):
    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind socket to listener address
    sock.bind(listener_address)

    # create a dictionary to map addresses for forwarding
    forward_map = dict()

    # read data and print to terminal
    while True:
        print('Waiting for message...')
        message_data, source_address = sock.recvfrom(1024)
        print(f'Received packet: {message_data}; from source: {source_address}')

        # the first message received will be from the client to the server
        # all messages are between the client and the server
        # we populate our forwarding map 
        if not forward_map:
            client_address = source_address
            forward_map[client_address] = server_address
            forward_map[server_address] = client_address

        # get the address to forward to and forward the packet
        destination_address = forward_map[source_address]
        Thread(target=forward, args=(sock, message_data, destination_address, drop_rate, delay)).start()


# example to run it with some hardcoded parameters
if __name__ == "__main__":
    server_address = ('127.0.0.1', 5006)
    listener_address = ('127.0.0.1', 5007)
    begin(listener_address=listener_address, server_address=server_address, drop_rate=0.0, delay=0.5)
