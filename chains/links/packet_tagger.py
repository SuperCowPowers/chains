"""PacketTagger: Add tags to incoming packets"""
import socket
import logging

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils
log_utils.log_defaults()


class PacketTagger(link.Link):
    """Add tags to incoming packets"""

    def __init__(self, tag_methods=None):
        """Initialize PacketTagger Class

           Args:
               tag_methods: a dictionary of {'field_name': method} (e.g. {'IP.src_domain': tag_domain})
                            Note: all methods must take the field value as an argmument (e.g. tag_domain(domain))
        """
        # Call super class init
        super(PacketTagger, self).__init__()

        self.tag_methods = tag_methods

        # Set my output
        self.output_stream = self._tag_stuff()

    def _tag_stuff(self):
        """Look through my input stream for the fields to be tagged"""

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # Make sure it has a tags field (which is a set)
            if 'tags' not in item:
                item['tags'] = set()

            # For each field in tag_methods call the method on that field
            if self.tag_methods:
                for field, method in self.tag_methods.iteritems():
                    self._field_action(item, field, method)

            # All done
            yield item

    def _field_action(self, item, key, action):
        """Follow the dot notation to get the proper field, then perform the action

           Args:
               item: the item in the input stream
               key: the key into the item that gives the field (IP.src)
               action: a method that takes the field and performs some action
        """
        ref = item
        try:
            for subkey in key.split('.')[:-1]:
                if isinstance(ref, dict):
                    ref = ref[subkey]
                else:
                    logging.critical('Cannot use subkey %s on non-dictionary element', subkey)
            subkey = key.split('.')[-1]
            value = ref[subkey]

            # Tag it
            item['tags'].add(action(value))

        # In general KeyErrors are expected
        except KeyError:
            pass

def tag_domain(domain):
    """Create a tag base on the domain field"""
    if domain == 'LOCAL':
        return 'local'
    elif domain == 'NXDOMAIN':
        return 'nxdomain'
    else:
        return 'external'

def test():
    """Test for PacketTagger class"""
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.links import reverse_dns
    import pprint

    # Create a PacketStreamer, a PacketMeta, and link them to PacketTagger
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()

    # Set up my tagging methods
    tag_methods = {'IP.src_domain': tag_domain, 'IP.dst_domain': tag_domain,
                   'IP6.src_domain': tag_domain, 'IP6.dst_domain': tag_domain}
    tagger = PacketTagger(tag_methods=tag_methods)

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tagger.link(rdns)

    for item in tagger.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
