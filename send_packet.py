import rdt_headers

def send_ack(sock, address, sequence_number):
    send_message(sock, address, sequence_number, 'ACK')
  
def send_nack(sock, address, sequence_number):
    send_message(sock, address, sequence_number, 'NACK')
  
def send_message(sock, address, sequence_number, message):
    bytes_message = bytes(message, 'utf-8')
    header = rdt_headers.make_header(sequence_number, bytes_message)
    packet = header + bytes_message
    sock.sendto(packet, address)
