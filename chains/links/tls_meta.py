"""TLSMeta: Pull out HTTP meta data from incoming flow data"""
import dpkt

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, data_utils
logger = log_utils.get_logger()


class TLSMeta(link.Link):
    """Pull out application meta data from incoming flow data"""

    def __init__(self):
        """Initialize TLSMeta Class"""

        # Call super class init
        super(TLSMeta, self).__init__()

        # Set my output
        self.output_stream = self._tls_meta_data()

    def _tls_meta_data(self):
        """Pull out the TLS metadata for each flow in the input_stream"""

        # For each flow process the contents
        for flow in self.input_stream:

            # Just TCP for now
            if flow['protocol'] != 'TCP':
                continue

            # Client to Server
            if flow['direction'] == 'CTS':

                # Try to process the payload as a set of TLS records
                try:
                    tls_records, bytes_consumed = dpkt.ssl.tls_multi_factory(flow['payload'])
                    if bytes_consumed != len(flow['payload']):
                        logger.warning('Incomplete TLS record at the end...')

                    # Process the TLS records
                    flow['tls'] = {'type':'TLS_CTS', 'data':{'tls_records': tls_records, 'uri':None, 'headers':None}}
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError, dpkt.ssl.SSL3Exception):
                    flow['tls'] = None

            # Server to Client
            else:
                try:
                    tls_records, bytes_consumed = dpkt.ssl.tls_multi_factory(flow['payload'])
                    if bytes_consumed != len(flow['payload']):
                        logger.warning('Incomplete TLS record at the end...')

                    # Process the TLS records
                    flow['tls'] = {'type':'TLS_STC', 'data':{'tls_records': tls_records, 'uri':None, 'headers':None}}
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError, dpkt.ssl.SSL3Exception):
                    flow['tls'] = None

            # All done
            yield flow

    def ssl_handshake_processing(tls_records):
        """Process a set of TLS records for a SSL handshake
           In general the order of messages should be the following:
           ClientHello, ServerHello, ServerKeyExchange, ServerHelloDone,
           ClientKeyExchange, ChangeCipherSpec, Finished, ChangeCipherSpec, Finished.
        """
        pass


def test():
    """Test for TLSMeta class"""

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta, reverse_dns, transport_meta, flows

    # Create a PacketStreamer, a PacketMeta, and link them to TLSMeta
    data_path = file_utils.relative_dir(__file__, '../../data/https.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10000)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = transport_meta.TransportMeta()
    fmeta = flows.Flows()
    tls_meta = TLSMeta()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)
    fmeta.link(tmeta)
    tls_meta.link(fmeta)

    # Print out the tags
    for item in tls_meta.output_stream:
        if item['tls']:
            tls_records = item['tls']['data']['tls_records']
            if item['tls']['type'] == 'TLS_CTS':
                print 'HTTPS_REQUEST'
                print '\t%s --> %s (%s) tls_records(%d)\n' % (item['src'], item['dst'], item['dst_domain'], len(tls_records))
            else:
                print 'HTTPS_RESPONSE'
                print '\t%s (%s) --> %s tls_records(%d)\n' % (item['src'], item['src_domain'], item['dst'], len(tls_records))
        else:
            logger.info('Could not find TLS in Flow:')
            flows.print_flow_info(item)

if __name__ == '__main__':
    test()
