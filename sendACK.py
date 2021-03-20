def send_ack(sock, address, sequence_number):
  ack_header = rdt_headers.make_header(sequence_number, 'ACK')
  ack_packet = ack_header + 'ACK'
  sock.sendto(ack_packet, address)
  
def send_nack(sock, address, sequence_number):
  ack_header = rdt_headers.make_header(sequence_number, 'NACK')
  ack_packet = ack_header + 'NACK'
  sock.sendto(ack_packet, address)
  
def send_message(sock, address, sequence_number, message):
  header = rdt_headers.make_header(sequence_number, message)
  packet = header + message
  sock.sendto(packet, address)
