import struct

RDT_HEADER_FORMAT = '!BH'

#calculates the checksum for a given sequence number and message
def calculate_checksum(sequence_number, message):
    def ones_complement_addition(a, b, modulus = 1<<16):
        result = a + b
        return result if result < modulus else (result + 1) % modulus

    #calculate a header for this packet as if there were no checksum
    pseudo_header = struct.pack(RDT_HEADER_FORMAT, sequence_number, 0)

    pseudo_packet = bytes(pseudo_header + message)

    #pad pseudo packet to be of even length
    if len(pseudo_packet) % 2 == 1:
        pseudo_packet += struct.pack('!B', 0)

    checksum = 0
    #iterate over the pseudo packet bytes two at a time
    for byte1, byte2 in zip(pseudo_packet[0::2], pseudo_packet[1::2]):
        #calculate the 16 bit representation of these two bytes 
        two_bytes = (byte1 << 8) + byte2
        #accumulate the pseudo_packet two bytes at a time using ones complement addition a la UDP checksum
        checksum = ones_complement_addition(checksum, two_bytes)

    #take the ones complement of the checksum to prevent 0 checksum
    checksum = ~checksum & 0xFFFF

    return checksum

#verifies that the given checksum matches the expected checksum for the sequence number and message
def is_valid_checksum(checksum, sequence_number, message):
    expected_checksum = calculate_checksum(sequence_number, message)
    return checksum == expected_checksum

#construct and return the header for the given packet parameters
def make_header(sequence_number, message):
    checksum = calculate_checksum(sequence_number, message)

    #construct the rdt header by taking 8 bits of sequence number and 16 bits of checksum
    return struct.pack(RDT_HEADER_FORMAT, sequence_number, checksum)

#retursn the checksum, sequence number, and message from a given rdt packet
def parse_rdt_packet(packet):
    #the header is the first three bytes of the packet
    header = packet[0:3]
    #unpack the header into the sequence number and checksum
    sequence_number, checksum = struct.unpack(RDT_HEADER_FORMAT, header)

    #the message is the rest of the packet
    message = packet[3:]

    #return the components of the packet
    return checksum, sequence_number, message

