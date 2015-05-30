"""Tagger: Add tags to incoming network data"""
import socket
import logging

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils
log_utils.log_defaults()


class Tagger(link.Link):
    """Add tags to incoming network data"""

    def __init__(self, tag_methods=None, default_tags=True):
        """Initialize Tagger Class

           Args:
               tag_methods: a dictionary of {'field_name': method} (e.g. {'IP.src_domain': tag_domain})
                            Note: all methods must take the field value as an argmument (e.g. tag_domain(domain))
        """
        # Call super class init
        super(Tagger, self).__init__()

        # Set up the complete tag dictionary
        self.tag_methods = {}
        if default_tags:
            self.tag_methods.update(self._defaults_tags())
        if tag_methods:
            self.tag_methods.update(tag_methods)

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
            for name, tag_method in self.tag_methods.iteritems():
                item['tags'].add(tag_method(item))

            # Not interested in None tags
            if None in item['tags']:
                item['tags'].remove(None)
            # All done
            yield item

    @staticmethod
    def value(data, key):
        """Follow the dot notation to get the proper field, then perform the action

           Args:
               data: the data as a dictionary (required to be a dictionary)
               key: the key into the data that gives the field (IP.src)

            Returns:
               the value of the field(subfield) if it exist, otherwise None
        """
        ref = data
        try:
            for subkey in key.split('.')[:-1]:
                if isinstance(ref, dict):
                    ref = ref[subkey]
                else:
                    logging.critical('Cannot use subkey %s on non-dictionary element', subkey)
            subkey = key.split('.')[-1]
            return ref[subkey]

        # In general KeyErrors are expected
        except KeyError:
            None
    
    @staticmethod
    def _defaults_tags():
        return {'direction': Tagger._tag_direction, 'nxdomain': Tagger._tag_nxdomain}

    @staticmethod
    def _tag_direction(data):
        """Create a tag based on the direction of the traffic"""

        # IP or IPv6
        src = Tagger.value(data, 'IP.src_domain') or Tagger.value(data, 'IP6.src_domain')
        dst = Tagger.value(data, 'IP.dst_domain') or Tagger.value(data, 'IP6.dst_domain')
        if src=='LOCAL':
            if dst=='LOCAL' or 'multicast' in dst or 'broadcast' in dst:
                return 'internal'
            else:
                return 'outgoing'
        elif dst=='LOCAL':
            return 'incoming'
        else:
            return 'direction_unknown'

    @staticmethod
    def _tag_nxdomain(data):
        """Create a tag based on whether there's an nxdomain present"""

        # IP or IPv6
        src = Tagger.value(data, 'IP.src_domain') or Tagger.value(data, 'IP6.src_domain')
        dst = Tagger.value(data, 'IP.dst_domain') or Tagger.value(data, 'IP6.dst_domain')
        if src=='NXDOMAIN' or dst=='NXDOMAIN':
            return 'nxdomain'
        else:
            return None

def test():
    """Test for Tagger class"""
    import pprint

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.links import reverse_dns
    from chains.utils import net_utils
    

    # Create a PacketStreamer, a PacketMeta, and link them to Tagger
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()

    # Have the tagger use its default tagging methods + my silly example
    def tag_is_tcp(data):
        return 'TCP' if Tagger.value(data, 'TCP') else None

    tags = Tagger() # Will use default tags
    tags2 = Tagger(tag_methods={'tcp': tag_is_tcp}, default_tags=False) # No default, just mine

    # Set up chain with 2 taggers!
    meta.link(streamer)
    rdns.link(meta)
    tags.link(rdns)
    tags2.link(tags)

    # So now you'll see tags from both taggers, the example is contrived but you can
    # see how easy it is to combine taggers so try to make your own!
    for item in tags2.output_stream:
        src = item[item['packet_type']]['src']
        dst = item[item['packet_type']]['dst']
        print '%s --> %s  Tags: %s' % (net_utils.ip_to_str(src), net_utils.ip_to_str(dst), str(list(item['tags'])))

if __name__ == '__main__':
    test()
