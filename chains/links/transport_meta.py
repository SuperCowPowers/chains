"""TransportMeta: Add tags to incoming packet data"""
import dpkt

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils, data_utils
log_utils.log_defaults()


class TransportMeta(link.Link):
    """Add tags to incoming packet data"""

    def __init__(self):
        """Initialize TransportMeta Class"""

        # Call super class init
        super(TransportMeta, self).__init__()

        # Set my output
        self.output_stream = self._transport_meta_data()

    def _transport_meta_data(self):
        """Pull out the transport metadata for each packet in the input_stream"""

        # For each packet in the pcap process the contents
        for item in self.input_stream:

            # Get the transport data and type
            trans_data = item['packet']['data']
            trans_type = self._get_transport_type(trans_data)
            item['transport'] = {'type': trans_type}
            if item['transport']['type']:
                item['transport'].update(data_utils.make_dict(trans_data))
                item['transport']['flags'] = self._readable_flags(item['transport'])
                item['transport']['direction'] = self._cts_or_stc(item)

            # All done
            yield item

    @staticmethod
    def _get_transport_type(transport):
        """Give the transport as a string or None if not one"""
        return transport.__class__.__name__  if transport.__class__.__name__ != 'str' else None

    @staticmethod
    def _readable_flags(transport):
        """Method that turns bit flags into a human readable list

           Args:
               transport (dict): transport info, specifically needs a 'flags' key with bit_flags
           Returns:
               list: a list of human readable flags (e.g. ['syn_ack', 'fin', 'rst', ...]
        """
        if 'flags' not in transport:
            return None
        _flag_list = []
        flags = transport['flags']
        if flags & dpkt.tcp.TH_SYN:
            if flags & dpkt.tcp.TH_ACK:
                _flag_list.append('syn_ack')
            else:
                _flag_list.append('syn')
        elif flags & dpkt.tcp.TH_FIN:
            if flags & dpkt.tcp.TH_ACK:
                _flag_list.append('fin_ack')
            else:
                _flag_list.append('fin')
        elif flags & dpkt.tcp.TH_RST:
            _flag_list.append('rst')
        return _flag_list

    @staticmethod
    def _cts_or_stc(data):
        """Does the data look like a Client to Server (cts) or Server to Client (stc) traffic?"""

        # Tests for TCP
        if data['transport']['type'] == 'TCP':
            flags = data['transport']['flags']

            # Syn/Ack or fin/ack is a server response
            if 'syn_ack' in flags or 'fin_ack' in flags:
                return 'stc'

            # Syn or fin is a client response
            if 'syn' in flags or 'fin' in flags:
                return 'cts'

        # Now make some educated guesses :)

        # IP or IPv6
        if 'src' in data['packet'] and 'dst' in data['packet']:
            src = net_utils.ip_to_str(data['packet']['src'])
            dst = net_utils.ip_to_str(data['packet']['dst'])

            # Internal talking to external?
            if net_utils.is_internal(src) and not net_utils.is_internal(dst):
                return 'cts'

            # External talking to internal?
            if net_utils.is_internal(dst) and not net_utils.is_internal(src):
                return 'stc'

        # UDP or TCP
        if 'sport' in data['transport']:
            sport = data['transport']['sport']
            dport = data['transport']['dport']

            # High port talking to low port
            if dport < 1024 and sport > dport:
                return 'cst'

            # Low port talking to high port
            if sport < 1024 and sport < dport:
                return 'stc'

        # Okay we have no idea so just return cts
        return 'cts'

def test():
    """Test for TransportMeta class"""
    import pprint

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.links import reverse_dns

    # Create a PacketStreamer, a PacketMeta, and link them to TransportMeta
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    trans_meta = TransportMeta()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    trans_meta.link(rdns)

    # Print out the tags
    for item in trans_meta.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
