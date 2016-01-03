"""ReverseDNS: Perform a reverse dns lookup on fields in the ip_field_list"""
import socket

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils, cache
log_utils.get_logger()


class ReverseDNS(link.Link):
    """Perform a reverse dns lookup on fields in the ip_field_list"""

    def __init__(self, domain_postfix='_domain'):
        """Initialize ReverseDNS Class

           Args:
               domain_postfix: the string to be appended to the ip fields (e.g. IP.src -> IP.src_domain)
        """
        # Call super class init
        super(ReverseDNS, self).__init__()

        self.domain_postfix = domain_postfix
        self.ip_lookup_cache = cache.Cache(timeout=600)

        # Set my output
        self.output_stream = self._process_for_rdns()

    def _process_for_rdns(self):
        """Look through my input stream for the fields in ip_field_list and
           try to do a reverse dns lookup on those fields.
        """

        # For each packet process the contents
        for item in self.input_stream:

            # Do for both the src and dst
            for endpoint in ['src', 'dst']:

                # Sanity check (might be an ARP, whatever... without a src/dst)
                if endpoint not in item['packet']:

                    # Set the domain to None
                    item['packet'][endpoint+self.domain_postfix] = None
                    continue

                # Convert inet_address to str ip_address
                ip_address = net_utils.inet_to_str(item['packet'][endpoint])

                # Is this already in our cache
                if self.ip_lookup_cache.get(ip_address):
                    domain = self.ip_lookup_cache.get(ip_address)

                # Is the ip_address local or special
                elif net_utils.is_internal(ip_address):
                    domain = 'internal'
                elif net_utils.is_special(ip_address):
                    domain = net_utils.is_special(ip_address)

                # Look it up at this point
                else:
                    domain = self._reverse_dns_lookup(ip_address)

                # Set the domain
                item['packet'][endpoint+self.domain_postfix] = domain

                # Cache it
                self.ip_lookup_cache.set(ip_address, domain)

            # All done
            yield item

    @staticmethod
    def _reverse_dns_lookup(ip_address):
        """Perform the reverse DNS lookup

           Args:
               ip_address: the ip_address (as a str)
           Returns:
               the domain given by a reverse DNS request on the ip address
        """

        # Look it up
        try:
            return socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            return 'nxdomain'

def test():
    """Test for ReverseDNS class"""
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    import pprint

    # Create a PacketStreamer, a PacketMeta, and link them to ReverseDNS
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=50)
    meta = packet_meta.PacketMeta()
    dns = ReverseDNS()

    meta.link(streamer)
    dns.link(meta)

    for item in dns.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
