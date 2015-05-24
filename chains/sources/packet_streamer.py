#!/usr/bin/env python
""" PacketStreamer: Use pcapy to stream packets from a network interface """
import pcap

# Local imports
from chains.sources import source
from chains.utils import file_utils

class PacketStreamer(source.Source):
    """Stream out the packets from the given network interface

       Args:
            iface_name: the network interface to capture packets from (defaults to None)
                        Note: None (not setting it) will open the first available network interface
                              You can also set this to a filename (iface_name = 'test.pcap')
            max_packets: set the maximum number of packets to yield (default to None)
     """


    def __init__(self, iface_name=None, max_packets=None):
        """Initialization for PacketStreamer"""

        # Call super class init
        super(PacketStreamer, self).__init__()

        self.iface_name = iface_name
        self.max_packets = max_packets
        self._output_stream = self._read_interface()

    def _read_interface(self):
        """Read Packets from the packet capture interface"""

        # Spin up the packet capture
        pc = pcap.pcap(name=self.iface_name, promisc=True, immediate=True)

        # For each packet in the pcap process the contents
        _packets = 0
        for timestamp, raw_buf in pc:
            yield {'timestamp': timestamp, 'raw_buf': raw_buf}
            _packets += 1
            if self.max_packets and _packets >= self.max_packets:
                raise StopIteration

def test():
    """Open up a test pcap file and stream the packets"""
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = PacketStreamer(iface_name=data_path, max_packets=10)
    for packet in streamer.output_stream:
        print packet

if __name__ == '__main__':
    test()
