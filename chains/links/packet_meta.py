#!/usr/bin/env python
"""PacketMeta: Use dpkt to pull out packet information"""
import dpkt
import datetime
import logging

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils
log_utils.log_defaults()

class PacketMeta(link.Link):
    """Use dpkt to pull out packet information"""

    def __init__(self):
        """Initialize PacketMeta Class"""

        # Call super class init
        super(PacketMeta, self).__init__()
        self._output_stream = self._packet_meta_data()

    def _packet_meta_data(self):
        """Pull out the metadata about each packet from the input_stream

           Args:
               packet_stream: a packet_stream yields packets (timestamp, buf)
        """

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

            # Make sure the Ethernet frame contains an IP packet
            # EtherType (IP, ARP, PPPoE, IP6... see http://en.wikipedia.org/wiki/EtherType)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                output['warning'] = 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
                logging.warning(output['warning'])
                yield output

            # Now unpack the data within the Ethernet frame (the IP packet)
            # Pulling out src, dst, length, fragment info, TTL, and Protocol
            ip = eth.data

            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            df = bool(ip.off & dpkt.ip.IP_DF)
            mf = bool(ip.off & dpkt.ip.IP_MF)
            offset = ip.off & dpkt.ip.IP_OFFMASK

            # IP Packet Info
            output['ip'] = {'src':ip.src, 'dst':ip.dst, 'len':ip.len, 'ttl':ip.ttl, 'df':df, 'mf': mf, 'offset': offset}
            yield output

def test():
    import pprint

    """Test for PacketMeta class"""
    from chains.sources import packet_streamer

    # Create a PacketStreamer and set its output to PacketMeta input
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')

    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = PacketMeta()
    meta.input_stream = streamer.output_stream
    for item in meta.output_stream:
        pprint.pprint(item)

if __name__ == '__main__':
    test()
