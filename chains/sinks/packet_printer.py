""" PacketPrinter: Prints out packet information """

# Local imports
from chains.sinks import sink
from chains.utils import net_utils

class PacketPrinter(sink.Sink):
    """Print packet information"""

    def __init__(self, color_output=True):
        """Initialize PacketPrinter Class"""

        # Call super class init
        super(PacketPrinter, self).__init__()

        # Should we add color on the output
        self._color = color_output

    def pull(self):
        """Print out information about each packet from the input_stream"""

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # Print out the timestamp in UTC
            print 'Timestamp: %s' % item['timestamp']

            # Unpack the Ethernet frame (mac src/dst, ethertype)
            print 'Ethernet Frame: %s --> %s  (type: %d)' % \
                  (net_utils.mac_to_str(item['eth']['src']), net_utils.mac_to_str(item['eth']['dst']), item['eth']['type'])

            # Print out the Packet info
            packet_type = item['packet']['type']
            print 'Packet: %s' % packet_type,
            packet = item['packet']
            if packet_type in ['IP', 'IP6']:
                print '%s --> %s (len:%d ttl:%d)' % (net_utils.inet_to_str(packet['src']), net_utils.inet_to_str(packet['dst']),
                                                     packet['len'], packet['ttl']),
                if packet_type == 'IP':
                    print '-- Frag(df:%d mf:%d offset:%d)' % (packet['df'], packet['mf'], packet['offset'])
                else:
                    print
            else:
                print str(packet)

            # Print out transport and application layers
            if item['transport']:
                transport_info = item['transport']
                print 'Transport: %s ' % transport_info['type'],
                for key, value in transport_info.iteritems():
                    if key != 'data':
                        print key+':'+repr(value),

                # Give summary info about data
                data = transport_info['data']
                print '\nData: %d bytes' % len(data),
                if data:
                    print '(%s...)' % repr(data)[:30]
                else:
                    print

            # Application data
            if item['application']:
                print 'Application: %s' % item['application']['type'],
                print str(item['application'])

            # Is there domain info?
            if 'src_domain' in packet:
                print 'Domains: %s --> %s' % (packet['src_domain'], packet['dst_domain'])

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

    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=50)
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
