""" PacketPrinter: Prints out packet information """
import pprint

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

            # Print out the Packet info (it's possible it's not there)
            '''
            packet_type = item['packet_type']
            print packet_type + ': ',
            if packet_type in item:
                packet = item[packet_type]
                print '%s --> %s (len:%d ttl:%d) -- Frag(df:%d mf:%d offset:%d)' % \
                      (net_utils.ip_to_str(packet['src']), net_utils.ip_to_str(packet['dst']), packet['len'], packet['ttl'], packet['df'], packet['mf'], ip['offset'])
            '''

            # Print out transport and application
            print 'Packet: %s' % item['packet_type']
            if item['packet_type']:
                pprint.pprint(item[item['packet_type']])
            print 'Transport: %s' % item['transport_type']
            if item['transport_type']:
                pprint.pprint(item[item['transport_type']])
            print 'Application: %s' % item['application_type']
            if item['application_type'] != 'UNKNOWN':
                pprint.pprint(item[item['application_type']])

def test():
    """Test for PacketPrinter class"""
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.utils import file_utils

    # Create a PacketStreamer and set its output to PacketPrinter input
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')

    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    printer = PacketPrinter()

    # Set up the chain
    meta.input_stream = streamer.output_stream
    printer.input_stream = meta.output_stream
    printer.pull()

if __name__ == '__main__':
    test()
