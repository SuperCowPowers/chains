"""PacketStreamer: Stream packets from a network interface"""
from __future__ import print_function
import os
import pcapy

# Local imports
from chains.sources import source
from chains.utils import file_utils, log_utils
logger = log_utils.get_logger()

class PacketStreamer(source.Source):
    """Stream out the packets from the given network interface

       Args:
            iface_name (str): The network interface to capture packets from (defaults to None). Note, by default it will
                              open the first available network interface. You can also set this to a filename (iface_name = 'test.pcap')
            bpf (str): BPF (Berkeley Packet Filter http://biot.com/capstats/bpf.html) (defaults to '*')
            max_packets (int): Set the maximum number of packets to yield (default to None)
     """

    def __init__(self, iface_name=None, bpf=None, max_packets=None):
        """Initialization for PacketStreamer"""

        # Call super class init
        super(PacketStreamer, self).__init__()

        # Check if the interface name was specified, if not set it to the first device
        if not iface_name:
            devices = pcapy.findalldevs()
            iface_name = devices[0]
            print('Auto Setting Interface to: {:s}'.format(iface_name))

        # Set parameters for capture interface
        self.iface_name = iface_name
        self.bpf = bpf
        self.max_packets = max_packets
        self.pcap = None
        self.output_stream = self.read_interface()

    def get_interface(self):
        """Get the current interface being captured

           Returns:
               The interface name as a str
        """
        return self.iface_name

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

    def read_interface(self):
        """Read Packets from the packet capture interface"""

        # Spin up the packet capture
        if self._iface_is_file():
            self.pcap = pcapy.open_offline(self.iface_name)
        else:
            try:
                # self.pcap = pcap.pcap(name=self.iface_name, promisc=True, immediate=True)
                #   snaplen (maximum number of bytes to capture _per_packet_)
                #   promiscious mode (1 for true)
                #   timeout (in milliseconds)
                self.pcap = pcapy.open_live(self.iface_name, 65536 , 1 , 0)
            except OSError:
                try:
                    logger.warning('Could not get promisc mode, turning flag off')
                    self.pcap = pcapy.open_live(self.iface_name, 65536 , 0 , 0)
                except OSError:
                    log_utils.panic('Could no open interface with any options (may need to be sudo)')

        # Add the BPF if it's specified
        if self.bpf:
            self.pcap.setfilter(self.bpf)
        print('listening on %s: %s' % (self.iface_name, self.bpf))

        # For each packet in the pcap process the contents
        _packets = 0
        while True:
            # Grab the next header and packet buffer
            header, raw_buf = self.pcap.next()

            # If we don't get a packet header break out of the loop
            if not header:
                break;

            # Extract the timestamp from the header and yield the packet
            seconds, micro_sec = header.getts()
            timestamp = seconds + micro_sec * 10**-6
            yield {'timestamp': timestamp, 'raw_buf': raw_buf, 'packet_num': _packets}
            _packets += 1

            # Is there a max packets set if so break on it
            if self.max_packets and _packets >= self.max_packets:
                break

        # All done so report and raise a StopIteration
        try:
            print('Packet stats: %d  received, %d dropped,  %d dropped by interface' % self.pcap.stats())
        except pcapy.PcapError:
            print('No stats available...')
        raise StopIteration

def test():
    """Open up a test pcap file and stream the packets"""

    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = PacketStreamer(iface_name=data_path, max_packets=50)
    for packet in streamer.output_stream:
        print(packet)

    # Test BPF Filter
    data_path = file_utils.relative_dir(__file__, '../../data/dns.pcap')
    streamer = PacketStreamer(iface_name=data_path, bpf='udp and dst port 53', max_packets=50)
    for packet in streamer.output_stream:
        print(packet)

if __name__ == '__main__':
    test()
