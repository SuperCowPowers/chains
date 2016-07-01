""" PacketStreamer: Stream packets from a network interface """
import os
import pcap

# Local imports
from chains.sources import source
from chains.utils import file_utils, log_utils
logger = log_utils.get_logger()

class PacketStreamer(source.Source):
    """Stream out the packets from the given network interface

       Args:
            iface_name: the network interface to capture packets from (defaults to None)
                        Note: None (not setting it) will open the first available network interface
                              You can also set this to a filename (iface_name = 'test.pcap')
            bpf: BPF (Berkeley Packet Filter http://biot.com/capstats/bpf.html) (defaults to '*')
            max_packets: set the maximum number of packets to yield (default to None)
     """

    def __init__(self, iface_name=None, bpf=None, max_packets=None):
        """Initialization for PacketStreamer"""

        # Call super class init
        super(PacketStreamer, self).__init__()

        self.iface_name = iface_name
        self.bpf = bpf
        self.max_packets = max_packets
        self.pcap = None
        self.output_stream = self._read_interface()

    def get_interface(self):
        """Get the current interface being captured

           Returns:
               The interface name as a str
        """
        return self.pcap.name

    def get_filter(self):
        """Get the current filter (BSP) being used (if any)

           Returns:
               The BSP filter specification
        """
        return self.pcap.filter

    def _iface_is_file(self):
        """Check if the iterface given is a file

           Returns:
                Boolean
        """
        return self.iface_name and os.path.isfile(self.iface_name)

    def _read_interface(self):
        """Read Packets from the packet capture interface"""

        # Spin up the packet capture
        if self._iface_is_file():
            self.pcap = pcap.pcap(name=self.iface_name)
        else:
            try:
                self.pcap = pcap.pcap(name=self.iface_name, promisc=True, immediate=True)
            except OSError:
                try:
                    logger.warning('Could not get immediate mode, turning flag off')
                    self.pcap = pcap.pcap(name=self.iface_name, promisc=True, immediate=False)
                except OSError:
                    try:
                        logger.warning('Could not get promisc  mode, turning flag off')
                        self.pcap = pcap.pcap(name=self.iface_name, promisc=False, immediate=False)
                    except OSError:
                        log_utils.panic('Could no open interface with any options (may need to be sudo)')

        # Add the BPF if it's specified
        if self.bpf:
            self.pcap.setfilter(self.bpf)
        print 'listening on %s: %s' % (self.pcap.name, self.pcap.filter)

        # For each packet in the pcap process the contents
        _packets = 0
        for timestamp, raw_buf in self.pcap:
            yield {'timestamp': timestamp, 'raw_buf': raw_buf, 'packet_num': _packets}
            _packets += 1
            if self.max_packets and _packets >= self.max_packets:
                try:
                    print ('Packet stats: %d  received, %d dropped,  %d dropped by interface') % self.pcap.stats()
                except OSError:
                    print ('No stats available...')
                raise StopIteration

def test():
    """Open up a test pcap file and stream the packets"""
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = PacketStreamer(iface_name=data_path, max_packets=50)
    for packet in streamer.output_stream:
        print packet

if __name__ == '__main__':
    test()
