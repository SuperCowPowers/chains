"""TransportMeta: Pull out transport meta data from incoming packet data"""
import dpkt

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, data_utils
log_utils.get_logger()


class TransportMeta(link.Link):
    """Pull out transport meta data from incoming packet data"""

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
            if trans_type and trans_data:
                item['transport'] = data_utils.make_dict(trans_data)
                item['transport']['type'] = trans_type
                item['transport']['flags'] = self._readable_flags(item['transport'])
                item['transport']['data'] = trans_data['data']

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
        elif flags & dpkt.tcp.TH_PUSH:
            _flag_list.append('psh')
        return _flag_list

def test():
    """Test for TransportMeta class"""
    import pprint

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta, reverse_dns

    # Create a PacketStreamer, a PacketMeta, and link them to TransportMeta
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=50)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = TransportMeta()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)

    # Print out the tags
    for item in tmeta.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
