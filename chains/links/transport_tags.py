"""TransportTags: Add tags to incoming packet data"""
import logging

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils
log_utils.log_defaults()


class TransportTags(link.Link):
    """Add tags to incoming packet data"""

    def __init__(self, add_tag_methods=None):
        """Initialize TransportTags Class

           Args:
               add_tag_methods: a list of additional tag methods (optional, defaults to None))
               Note: all methods must take the data dictionary as an argmument (e.g. tag_method(data))
        """
        # Call super class init
        super(TransportTags, self).__init__()

        # Set up the complete tag dictionary
        self.tag_methods = [self._cts_or_stc]
        if add_tag_methods:
            self.tag_methods += add_tag_methods

        # Set my output
        self.output_stream = self._tag_stuff()

    def _tag_stuff(self):
        """Look through my input stream for the fields to be tagged"""

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # Make sure it has a tags field (which is a set)
            if 'tags' not in item:
                item['tags'] = set()

            # For each tag_methods run it on the item
            for tag_method in self.tag_methods:
                item['tags'].add(tag_method(item))

            # Remove any None tags
            if None in item['tags']:
                item['tags'].remove(None)
            # All done
            yield item

    @staticmethod
    def _cts_or_stc(data):
        """Does the data look like a Client to Server (cts) or Server to Client (stc) traffic?"""

        # Tests for TCP
        if data['transport_type'] == 'TCP':
            flags = data[data['transport_type']]['flags']

            # Syn/Ack or fin/ack is a server response
            if 'syn_ack' in flags or 'fin_ack' in flags:
                return 'stc'

            # Syn or fin is a client response
            if 'syn' in flags or 'fin' in flags:
                return 'cts'

        # Now make some educated guesses :)

        # IP or IPv6
        src = data[data['packet_type']]['src']
        dst = data[data['packet_type']]['dst']

        # Internal talking to external?
        if net_utils.is_internal(src) and not net_utils.is_internal(dst):
            return 'cts'

        # External talking to internal?
        if net_utils.is_internal(dst) and not net_utils.is_internal(src):
            return 'stc'

        # UDP or TCP
        if 'sport' in data[data['transport_type']]:
            sport = data[data['transport_type']]['sport']
            dport = data[data['transport_type']]['dport']
    
            # High port talking to low port
            if dport < 1024 and sport > dport:
                return 'cst'
    
            # Low port talking to high port
            if sport < 1024 and sport < dport:
                return 'stc'

        # Okay we have no idea
        return None

def test():
    """Test for TransportTags class"""

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.links import reverse_dns

    # Create a PacketStreamer, a PacketMeta, and link them to TransportTags
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tags = TransportTags()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tags.link(rdns)

    # Print out the tags
    for item in tags.output_stream:
        src = item[item['packet_type']]['src']
        dst = item[item['packet_type']]['dst']
        print '%s --> %s  Tags: %s' % (net_utils.ip_to_str(src), net_utils.ip_to_str(dst), str(list(item['tags'])))

if __name__ == '__main__':
    test()
