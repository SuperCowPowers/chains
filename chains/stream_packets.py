#!/usr/bin/env python
"""
    Use pypcap to read in packets from the network interface and yield the raw buffers
"""
import pcap

def stream_packets(max_packets=None):
    """Stream out the packets from the given network interface

       Args:
           net_iface: the network interface to capture packets from
           max_packets: set the maximum number of packets to yield (default to None)
    """

    # Spin up the packet capture
    pc = pcap.pcap(promisc=True, immediate=True)

    # For each packet in the pcap process the contents
    _packets = 0
    for timestamp, buf in pc:
        yield timestamp, buf
        _packets += 1
        if max_packets and _packets >= max_packets:
            raise StopIteration

def test():
    """Open up a test pcap file and print out the packets"""
    for packet in stream_packets(max_packets=10):
        print packet

if __name__ == '__main__':
    test()
