"""ReverseDNS: Perform a reverse dns lookup on fields in the ip_field_list"""
import socket
import logging

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils
log_utils.log_defaults()


class ReverseDNS(link.Link):
    """Perform a reverse dns lookup on fields in the ip_field_list"""

    def __init__(self, ip_field_list=('IP.src', 'IP.dst', 'IP6.src', 'IP6.dst'), domain_postfix='_domain'):
        """Initialize ReverseDNS Class

           Args:
               ip_field_list: a tuple of fields in the input stream which contain ip addresses.
                              Use dotted notation for the field, defaults to ('IP.src', 'IP.dst', 'IP6.src, IP6.dst')
               domain_postfix: the string to be appended to the ip fields (e.g. IP.src -> IP.src_domain)
        """
        # Call super class init
        super(ReverseDNS, self).__init__()

        self.ip_field_list = ip_field_list
        self.domain_postfix = domain_postfix
        self.ip_lookup_cache = {}

        # Set my output
        self.output_stream = self._reverse_dns_lookup()

    def _reverse_dns_lookup(self):
        """Look through my input stream for the fields in ip_field_list and
           try to do a reverse dns lookup on those fields.
        """

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # For each field in ip_field_list do the reverse DNS lookup
            for field in self.ip_field_list:
                self._field_action(item, field, self._reverse_dns)

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
            ip_address = net_utils.ip_to_str(ref[subkey])

            # Is this already in our cache
            if ip_address in self.ip_lookup_cache:
                ref[subkey+self.domain_postfix] = self.ip_lookup_cache[ip_address]
                return

            # Is the ip_address local or special
            if self._is_local(ip_address):
                domain = 'LOCAL'
            elif self._is_special(ip_address):
                domain = self._is_special(ip_address)

            # Look it up
            else:
                domain = action(ip_address)

            # Set it and cache it
            ref[subkey+self.domain_postfix] = domain
            self.ip_lookup_cache[ip_address] = domain

        # All kinds of stuff might happen
        except KeyError:
            pass # In general KeyErrors are expected
        except ValueError as exc:
            logging.info('ValueError: %s', exc)
        except TypeError as exc:
            logging.info('TypeError: %s', exc)

    @staticmethod
    def _is_local(ip_address):
        """Determine if the address is LOCAL
           Note: This is super bad, improve it
        """
        # Local networks 10.0.0.0/8, 172.16.0.0/12, '192.168.0.0/16
        local_nets = '10.', '172.16.', '192.168.', '169.254', 'fd', 'fe80::'
        return any([ip_address.startswith(local) for local in local_nets])

    @staticmethod
    def _is_special(ip_address):
        """Determine if the address is SPECIAL
           Note: This is super bad, improve it
        """
        special = {'224.0.0.251': 'multicast_dns',
                   'ff02::fb': 'multicast_dns'}
        return special[ip_address] if ip_address in special else None

    @staticmethod
    def _reverse_dns(ip_address):
        """Actually perform the reverse DNS lookup"""
        if ReverseDNS._is_local(ip_address):
            return 'LOCAL'
        try:
            return socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            return 'NXDOMAIN'


def test():
    """Test for ReverseDNS class"""
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    import pprint

    # Create a PacketStreamer, a PacketMeta, and link them to ReverseDNS
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    dns = ReverseDNS()

    meta.link(streamer)
    dns.link(meta)

    for item in dns.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
