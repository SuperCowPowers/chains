"""DNSMeta: Pull out DNS meta data from incoming transport data"""
import dpkt
import urllib2

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, data_utils
logger = log_utils.get_logger()


class DNSMeta(link.Link):
    """Pull out DNS meta data from incoming packet/transport data"""

    def __init__(self):
        """Initialize DNSMeta Class"""

        # Call super class init
        super(DNSMeta, self).__init__()

        # Set my output
        self.output_stream = self._dns_meta_data()

    def _dns_meta_data(self):
        """Pull out the dns metadata for packet/transport in the input_stream"""

        # For each packet process the contents
        for packet in self.input_stream:
            if 'transport' not in packet:
                print 'Transport info not found in %s' % packet
            try:
                dns_meta = dpkt.dns.DNS(packet['transport']['data'])
                packet['dns'] = data_utils.make_dict(dns_meta)
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                packet['dns'] = None

            # All done
            yield packet


def test():
    """Test for DNSMeta class"""
    import pprint

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta, reverse_dns, transport_meta

    # Create a PacketStreamer, a PacketMeta, and link them to DNSMeta
    data_path = file_utils.relative_dir(__file__, '../../data/dns.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10000)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = transport_meta.TransportMeta()
    dns_meta = DNSMeta()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)
    dns_meta.link(tmeta)

    # Print out the tags
    for item in dns_meta.output_stream:
        if item['dns']:
            pprint.pprint(item['dns'])

if __name__ == '__main__':
    test()
