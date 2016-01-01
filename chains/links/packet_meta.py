"""PacketMeta: Use dpkt to pull out packet information"""
import dpkt
import datetime

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils, data_utils
logger = log_utils.get_logger()

class PacketMeta(link.Link):
    """Use dpkt to pull out packet information"""

    def __init__(self):
        """Initialize PacketMeta Class"""

        # Call super class init
        super(PacketMeta, self).__init__()

        # Set my output
        self.output_stream = self._packet_meta_data()

    def _packet_meta_data(self):
        """Pull out the metadata about each packet from the input_stream"""

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # Output object
            output = {}

            # Grab the fields I need
            timestamp = item['timestamp']
            buf = item['raw_buf']

            # Print out the timestamp in UTC
            output['timestamp'] = datetime.datetime.utcfromtimestamp(timestamp)

            # Unpack the Ethernet frame (mac src/dst, ethertype)
            eth = dpkt.ethernet.Ethernet(buf)
            output['eth'] = {'src': eth.src, 'dst': eth.dst, 'type':eth.type}

            # Grab packet data
            packet = eth.data

            # Packet Type ('EtherType') (IP, ARP, PPPoE, IP6... see http://en.wikipedia.org/wiki/EtherType)
            if hasattr(packet, 'data'):
                output['packet'] = {'type': packet.__class__.__name__, 'data': packet.data}
            else:
                output['packet'] = {'type': None, 'data': None}

            # It this an IP packet?
            if output['packet']['type'] == 'IP':

                # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
                df = bool(packet.off & dpkt.ip.IP_DF)
                mf = bool(packet.off & dpkt.ip.IP_MF)
                offset = packet.off & dpkt.ip.IP_OFFMASK

                # Pulling out src, dst, length, fragment info, TTL, checksum and Protocol
                output['packet'].update({'src':packet.src, 'dst':packet.dst, 'p': packet.p, 'len':packet.len, 'ttl':packet.ttl,
                                         'df':df, 'mf': mf, 'offset': offset, 'checksum': packet.sum})

            # Is this an IPv6 packet?
            elif output['packet']['type'] == 'IP6':

                # Pulling out the IP6 fields
                output['packet'].update({'src':packet.src, 'dst':packet.dst, 'p': packet.p, 'len':packet.plen, 'ttl':packet.hlim})

            # If the packet isn't IP or IPV6 just pack it as a dictionary
            else:
                output['packet'].update(data_utils.make_dict(packet))

            # For the transport layer we're going to set the transport to None. and
            # hopefully a 'link' upstream will manage the transport functionality
            output['transport'] = None

            # For the application layer we're going to set the application to None. and
            # hopefully a 'link' upstream will manage the application functionality
            output['application'] = None

            # All done
            yield output

def test():
    """Test for PacketMeta class"""
    from chains.sources import packet_streamer
    import pprint

    # Create a PacketStreamer and set its output to PacketMeta input
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=50)

    meta = PacketMeta()
    meta.link(streamer)

    for item in meta.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
