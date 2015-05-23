#!/usr/bin/env python
"""
    Use pypcap to read in packets from the network interface and yield the raw buffers
"""
import pcap

# Local imports
from . import utils

def stream_packets(iface_name=None, max_packets=None):
    """Stream out the packets from the given network interface

       Args:
           iface_name: the network interface to capture packets from (defaults to None)
                       Note: None (not setting it) will open the first available network interface
                             You can also set this to a filename (iface_name = 'test.pcap')
           max_packets: set the maximum number of packets to yield (default to None)
    """

    # Spin up the packet capture
    pc = pcap.pcap(name=iface_name, promisc=True, immediate=True)

    # For each packet in the pcap process the contents
    _packets = 0
    for timestamp, buf in pc:
        yield timestamp, buf
        _packets += 1
        if max_packets and _packets >= max_packets:
            raise StopIteration

def test():
    """Open up a test pcap file and print out the packets"""
    data_path = utils.relative_path(__file__, '../data/http.pcap')
    for packet in stream_packets(iface_name = data_path, max_packets=10):
        print packet

if __name__ == '__main__':
    test()
