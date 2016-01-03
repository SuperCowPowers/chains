"""PacketTags: Add tags to incoming packet data"""

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils
logger = log_utils.get_logger()


class PacketTags(link.Link):
    """Add tags to incoming packet data"""

    def __init__(self, add_tag_methods=None):
        """Initialize PacketTags Class

           Args:
               add_tag_methods: a list of additional tag methods (optional, defaults to None))
               Note: all methods must take the data dictionary as an argmument (e.g. tag_method(data))
        """
        # Call super class init
        super(PacketTags, self).__init__()

        # Set up the complete tag dictionary
        self.tag_methods = [PacketTags._tag_net_direction, PacketTags._tag_nxdomain]
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

            # Not interested in None tags
            if None in item['tags']:
                item['tags'].remove(None)
            # All done
            yield item

    @staticmethod
    def _tag_net_direction(data):
        """Create a tag based on the direction of the traffic"""

        # IP or IPv6
        src = data['packet']['src_domain']
        dst = data['packet']['dst_domain']
        if src == 'internal':
            if dst == 'internal' or 'multicast' in dst or 'broadcast' in dst:
                return 'internal'
            else:
                return 'outgoing'
        elif dst == 'internal':
            return 'incoming'
        else:
            return None

    @staticmethod
    def _tag_nxdomain(data):
        """Create a tag based on whether there's an nxdomain present"""

        # IP or IPv6
        src = data['packet']['src_domain']
        dst = data['packet']['dst_domain']
        if src == 'nxdomain' or dst == 'nxdomain':
            return 'nxdomain'
        else:
            return None

def test():
    """Test for PacketTags class"""

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.links import reverse_dns

    # Create a PacketStreamer, a PacketMeta, and link them to PacketTags
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=50)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()

    # Have the PacketTags use its default tagging methods + my silly example
    def tag_is_tcp(data):
        return 'Wow! IP' if data['packet']['type'] == 'IP' else None

    tags = PacketTags(add_tag_methods=[tag_is_tcp]) # Add my silly tag

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tags.link(rdns)

    # Print out the tags
    for item in tags.output_stream:
        src = item['packet']['src']
        dst = item['packet']['dst']
        print '%s --> %s  Tags: %s' % (net_utils.inet_to_str(src), net_utils.inet_to_str(dst), str(list(item['tags'])))

if __name__ == '__main__':
    test()
