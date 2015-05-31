"""PacketMeta: Use dpkt to pull out packet information"""
import dpkt
import datetime
import logging

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils
log_utils.log_defaults()

class PacketMeta(link.Link):
    """Use dpkt to pull out packet information"""

    def __init__(self):
        """Initialize PacketMeta Class"""

        # Call super class init
        super(PacketMeta, self).__init__()

        # Set my output
        self.output_stream = self._packet_meta_data()

    @staticmethod
    def _make_dict(obj):
        """This method creates a dictionary out of an object"""
        return {key: getattr(obj, key) for key in dir(obj) if not key.startswith('__') and not callable(getattr(obj, key))}

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

            # EtherType (IP, ARP, PPPoE, IP6... see http://en.wikipedia.org/wiki/EtherType)
            output['packet_type'] = eth.data.__class__.__name__

            # Grab packet data
            packet = eth.data

            # It this an IP packet?
            if output['packet_type'] == 'IP':

                # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
                df = bool(packet.off & dpkt.ip.IP_DF)
                mf = bool(packet.off & dpkt.ip.IP_MF)
                offset = packet.off & dpkt.ip.IP_OFFMASK

                # Pulling out src, dst, length, fragment info, TTL, checksum and Protocol
                output[output['packet_type']] = {'src':packet.src, 'dst':packet.dst, 'p': packet.p, 'len':packet.len, 'ttl':packet.ttl,
                                                 'df':df, 'mf': mf, 'offset': offset, 'checksum': packet.sum}

            # Is this an IPv6 packet?
            elif output['packet_type'] == 'IP6':

                # Pulling out the IP6 fields
                output[output['packet_type']] = {'src':packet.src, 'dst':packet.dst, 'p': packet.p, 'len':packet.plen, 'ttl':packet.hlim}

            # If the packet isn't IP or IPV6 just pack it as a dictionary
            else:
                output[output['packet_type']] = self._make_dict(packet)

            # For the transport layers we're going to make the TCP flags 'human readable' but for
            # everything else we're just going to bundle up the object as a dictionary
            try:
                transport = packet.data
                output['transport_type'] = self._transport(packet)
                if output['transport_type']:
                    output[output['transport_type']] = self._make_dict(transport)
                    output[output['transport_type']]['flags'] = self._readable_flags(output[output['transport_type']])
            except AttributeError: # No packet data
                output['transport_type'] = None

            # For the application layer we're going to set the appliction_type to None. and
            # hopefully a 'link' upstream will manage the application identification functionality
            output['application_type'] = None

            # All done
            yield output

    @staticmethod
    def _transport(packet):
        """Give the transport as a string or None if not one"""
        return packet.data.__class__.__name__  if packet.data.__class__.__name__ != 'str' else None

    @staticmethod
    def _readable_flags(transport):
        """Method that turns bit flags into a human readable list

           Args:
               flags = bit_flags
           Returns:
               a list of human readable flags (e.g. ['syn_ack', 'fin', 'rst', ...]
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

def test():
    """Test for PacketMeta class"""
    from chains.sources import packet_streamer
    import pprint

    # Create a PacketStreamer and set its output to PacketMeta input
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)

    meta = PacketMeta()
    meta.link(streamer)

    for item in meta.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
