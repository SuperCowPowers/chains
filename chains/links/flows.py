"""Flows: Takes an input_stream of packets and provides an output_stream of flows
          based on (src, dst, src_port, dst_port, protocol) flow ids.
"""


import time
from collections import defaultdict

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, net_utils, flow_utils
log_utils.get_logger()


class Flows(link.Link):
    """Flows: Takes an input_stream of packets and provides an output_stream of flows
              based on (src, dst, src_port, dst_port, protocol) flow ids.
    """

    def __init__(self):
        """Initialize Flows Class"""

        # Call super class init
        super(Flows, self).__init__()

        # Flows
        self._flows = defaultdict(flow_utils.Flow)

        # Set my output
        self.output_stream = self._packets_to_flows()

    def _packets_to_flows(self):
        """Combine packets into flows"""

        # For each packet, place it into either an existing flow or a new flow
        for packet in self.input_stream:

            # Compute flow tuple and add the packet to the flow
            flow_id = flow_utils.flow_tuple(packet)
            self._flows[flow_id].add_packet(packet)

            # Yield flows that are ready to go
            for flow in self._flows.values():
                if flow.ready():
                    flow_info = flow.get_flow()
                    yield flow_info
                    del self._flows[flow_info['flow_id']]

        # All done so just dump what we have left
        print '---- NO MORE INPUT ----'
        for flow in sorted(self._flows.values(), key=lambda x: x.meta['start']):
            yield flow.get_flow()

def print_flow_info(flow):
    """Print a summary of the flow inforamtion"""
    print 'Flow %s (%s)-- Packets:%d Bytes:%d Payload: %s...' % (flow['flow_id'], flow['direction'], len(flow['packet_list']),
                                                              len(flow['payload']), repr(flow['payload'])[:30])

def test():
    """Test for Flows class"""
    import pprint

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta, reverse_dns, transport_meta

    # Create a PacketStreamer, a PacketMeta, and link them to TransportMeta
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=1000)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = transport_meta.TransportMeta()
    flows = Flows()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)
    flows.link(tmeta)

    # Print out the flow information
    for flow in flows.output_stream:
        print_flow_info(flow)

if __name__ == '__main__':
    test()
