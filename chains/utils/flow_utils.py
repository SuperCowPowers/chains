"""Flow class for aggregating packets into a Flow"""

from datetime import datetime, timedelta
from collections import defaultdict

# Local imports
from chains.utils import file_utils, net_utils

# Helper methods
def flow_tuple(data):
    """Tuple for flow (src, dst, sport, dport, proto)"""
    return (data['packet']['src'], data['packet']['dst'], data['transport'].get('sport'),
            data['transport'].get('dport'), data['transport']['type'])

def _flow_tuple_reversed(f_tuple):
    """Reversed tuple for flow (dst, src, dport, sport, proto)"""
    return (f_tuple[1], f_tuple[0], f_tuple[3], f_tuple[2], f_tuple[4])

class Flow(object):
    """Flow object"""

    def __init__(self):
        """Initialize Flow Class"""

        # Set up my meta data
        self._flow_id = None
        self._protocol = None
        self._direction = None
        self._packet_list = []
        self._payload = ''
        self._start = None
        self._end = None
        self._timeout = datetime.now() + timedelta(seconds=1)

    def add_packet(self, packet):
        """Add a packet to this flow"""

        # First packet?
        if not self._flow_id:
            self._flow_id = flow_tuple(packet)
            self._protocol = packet['transport']['type']
            self._direction = self._cts_or_stc(packet)
            self._start = packet['timestamp']
            self._end = packet['timestamp']

        # Add the packet
        self._packet_list.append(packet)
        if packet['timestamp'] < self._start:
            self._start = packet['timestamp']
        if packet['timestamp'] > self._end:
            self._end = packet['timestamp']

    def get_flow(self):
        """Reassemble the flow and return all the info/data"""
        if self._protocol == 'TCP':
            self._packet_list.sort(key=lambda packet: packet['transport']['seq'])

        # Join the packet data into one payload
        for packet in self._packet_list:
            self._payload += packet['transport']['data']

        return {'flow': self._flow_id, 'num_packets': len(self._packet_list), 'bytes': len(self._payload), 'payload': self._payload,
                'start_time': self._start, 'end_time': self._end}

    def timeout(self):
        """Has this flow been timed out?"""
        return  datetime.now() > self._timeout

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
        # Internal/External
        if 'src' in data['packet'] and 'dst' in data['packet']:
            src = net_utils.ip_to_str(data['packet']['src'])
            dst = net_utils.ip_to_str(data['packet']['dst'])

            # Internal talking to external?
            if net_utils.is_internal(src) and not net_utils.is_internal(dst):
                return 'cts'

            # External talking to internal?
            if net_utils.is_internal(dst) and not net_utils.is_internal(src):
                return 'stc'

        # Source Port/Destination Port
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
    """Test for the Flow class"""

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta, reverse_dns, transport_meta

    # Create a PacketStreamer, a PacketMeta, and link them to TransportMeta
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=50)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = transport_meta.TransportMeta()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)

    # Put the packets into flows
    flows = defaultdict(Flow)
    for packet in tmeta.output_stream:
        flow_id = flow_tuple(packet)
        flows[flow_id].add_packet(packet)

    # Print out flow information
    for flow in flows.values():
        fd = flow.get_flow()
        print 'Flow %s -- Packets:%d Bytes:%d Payload: %s' % (fd['flow'], fd['num_packets'], fd['bytes'], fd['payload'][:20])

if __name__ == '__main__':

    # Run the test
    test()
