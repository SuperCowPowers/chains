""" PacketSummary: Prints out packet information """

# Local imports
from chains.sinks import sink
from chains.utils import net_utils

class PacketSummary(sink.Sink):
    """Print packet information"""

    def __init__(self):
        """Initialize PacketSummary Class"""

        # Call super class init
        super(PacketSummary, self).__init__()

    def pull(self):
        """Print out summary information about each packet from the input_stream"""

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # Print out the timestamp in UTC
            print '%s -' % item['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),

            # Transport info
            if item['transport_type']:
                print item['transport_type'],

            # Print out the Packet info
            packet_type = item['packet_type']
            print packet_type,
            packet = item[packet_type]
            if packet_type in ['IP', 'IP6']:
                # Is there domain info?
                if 'src_domain' in packet:
                    print '%s(%s) --> %s(%s)' % (net_utils.ip_to_str(packet['src']), packet['src_domain'],
                                                 net_utils.ip_to_str(packet['dst']), packet['dst_domain']),
                else:
                    print '%s --> %s' % (net_utils.ip_to_str(packet['src']), net_utils.ip_to_str(packet['dst'])),
            else:
                print str(packet)

            # Only include application if we have it
            if item['application_type']:
                print 'Application: %s' % item['application_type'],
                print str(item[item['application_type']]),

            # Tags
            if 'tags' in item:
                print 'TAGS:', list(item['tags'])        

def test():
    """Test for PacketSummary class"""
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.links import reverse_dns
    from chains.utils import file_utils

    # Create a PacketStreamer and set its output to PacketSummary input
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')

    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    printer = PacketSummary()

    # Set up the chain
    meta.link(streamer)
    rdns.link(meta)
    printer.link(rdns)

    # Pull the chain
    printer.pull()

if __name__ == '__main__':
    test()
