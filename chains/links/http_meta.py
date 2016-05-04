"""HTTPMeta: Pull out HTTP meta data from incoming flow data"""
import dpkt
import urllib2

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, data_utils
logger = log_utils.get_logger()


class HTTPMeta(link.Link):
    """Pull out application meta data from incoming flow data"""

    def __init__(self):
        """Initialize HTTPMeta Class"""

        # Call super class init
        super(HTTPMeta, self).__init__()

        # Set my output
        self.output_stream = self._http_meta_data()

    def _http_meta_data(self):
        """Pull out the application metadata for each flow in the input_stream"""

        # For each flow process the contents
        for flow in self.input_stream:

            # Client to Server
            if flow['direction'] == 'CTS':
                try:
                    request = dpkt.http.Request(flow['payload'])
                    request_data = data_utils.make_dict(request)
                    request_data['uri'] = self._clean_uri(request['uri'])
                    flow['http'] = {'type':'HTTP_REQUEST', 'data':request_data}
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                    flow['http'] = None

            # Server to Client
            else:
                try:
                    response = dpkt.http.Response(flow['payload'])
                    flow['http'] = {'type': 'HTTP_RESPONSE', 'data': data_utils.make_dict(response)}
                except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                    flow['http'] = None

            # Mark non-TCP HTTP
            if flow['http'] and flow['protocol'] != 'TCP':
                flow['http'].update({'weird': 'UDP-HTTP'})

            # All done
            yield flow

    @staticmethod
    def _clean_uri(uri):
        """Clean the URI string"""
        return urllib2.unquote(uri).replace('+', ' ')


def test():
    """Test for HTTPMeta class"""

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta, reverse_dns, transport_meta, flows

    # Create a PacketStreamer, a PacketMeta, and link them to HTTPMeta
    data_path = file_utils.relative_dir(__file__, '../../data/http.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10000)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = transport_meta.TransportMeta()
    fmeta = flows.Flows()
    http_meta = HTTPMeta()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)
    fmeta.link(tmeta)
    http_meta.link(fmeta)

    # Print out the tags
    for item in http_meta.output_stream:
        if item['http']:
            print '%s %s --> %s  %s' % (item['http']['type'], item['src'], item['dst'], item['http']['data'])

if __name__ == '__main__':
    test()
