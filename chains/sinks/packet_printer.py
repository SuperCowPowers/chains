""" PacketPrinter: Prints out packet information """

# Local imports
from chains.sinks import sink
from chains.utils import net_utils

class PacketPrinter(sink.Sink):
    """Print packet information"""

    def __init__(self):
        """Initialize PacketPrinter Class"""

        # Call super class init
        super(PacketPrinter, self).__init__()


    def pull(self):
        """Print out information about each packet from the input_stream"""

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # Print out the timestamp in UTC
            print 'Timestamp: %s' % str(item['timestamp'])

            # Unpack the Ethernet frame (mac src/dst, ethertype)
            print 'Ethernet Frame: %s --> %s  (type: %d)' % \
                  (net_utils.mac_addr(item['eth']['src']), net_utils.mac_addr(item['eth']['dst']), item['eth']['type'])

            # Print out the Packet info
            packet_type = item['packet_type']
            print 'Packet: %s' % packet_type,
            packet = item[packet_type]
            if packet_type in ['IP', 'IP6']:
                print '%s --> %s (len:%d ttl:%d)' % (net_utils.ip_to_str(packet['src']), net_utils.ip_to_str(packet['dst']),
                                                     packet['len'], packet['ttl']),
                if packet_type == 'IP':
                    print '-- Frag(df:%d mf:%d offset:%d)' % (packet['df'], packet['mf'], packet['offset'])
                else:
                    print
                # Is there domain info?
                if 'src_domain' in packet:
                    print 'Domains: %s --> %s' % (packet['src_domain'], packet['dst_domain'])
            else:
                print str(packet)

            # Print out transport and application layers
            print 'Transport: %s' % item['transport_type'],
            if item['transport_type']:
                print str(item[item['transport_type']])
            print 'Application: %s' % item['application_type'],
            if item['application_type']:
                print str(item[item['application_type']])
            print

            # Tags
            if 'tags' in item:
                print list(item['tags'])
            print

def test():
    """Test for PacketPrinter class"""
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.links import reverse_dns
    from chains.utils import file_utils

    # Create a PacketStreamer and set its output to PacketPrinter input
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')

    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    printer = PacketPrinter()

    # Set up the chain
    meta.link(streamer)
    rdns.link(meta)
    printer.link(rdns)

    # Pull the chain
    printer.pull()

if __name__ == '__main__':
    test()
