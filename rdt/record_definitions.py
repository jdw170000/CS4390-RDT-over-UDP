from recordclass import recordclass

ClientStatistics = recordclass('ClientStatistics', 'numTransmits numRetransmits numTOevents numBytes numCorrupts elapsed')

ServerStatistics = recordclass('ServerStatistics', 'numBytes numErrors numOutOfSeq')

GBN_PacketDescriptor = recordclass('PacketDescriptor', 'message sequence_number')

SR_PacketDescriptor = recordclass('PacketDescriptor', 'message sequence_number acked timer')
