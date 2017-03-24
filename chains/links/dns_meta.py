"""DNSMeta, Pull out DNS meta data from incoming transport data"""
from __future__ import print_function
import math
from collections import Counter
import dpkt

# Local imports
from chains.links import link
from chains.utils import file_utils, log_utils, data_utils


class DNSMeta(link.Link):
    """Pull out DNS meta data from incoming packet/transport data"""

    def __init__(self):
        """Initialize DNSMeta Class"""

        # Call super class init
        super(DNSMeta, self).__init__()

        # Set my output
        self.output_stream = self.dns_meta_data()

        #
        # Maps for various flags/response codes
        #

        # Opcodes
        self.opcodes = {0:'DNS_QUERY', 1:'DNS_IQUERY', 2:'DNS_STATUS', 4:'DNS_NOTIFY', 5:'DNS_UPDATE'}

        # Response codes
        self.rcodes = {0:'DNS_RCODE_NOERR', 1:'DNS_RCODE_FORMERR', 2:'DNS_RCODE_SERVFAIL', 3:'DNS_RCODE_NXDOMAIN',
                       4:'DNS_RCODE_NOTIMP', 5:'DNS_RCODE_REFUSED', 6:'DNS_RCODE_YXDOMAIN', 7:'DNS_RCODE_YXRRSET',
                       8:'DNS_RCODE_NXRRSET', 9:'DNS_RCODE_NOTAUTH', 10:'DNS_RCODE_NOTZONE'}

        # Query Types
        self.query_types = {1:'DNS_A', 2:'DNS_NS', 5:'DNS_CNAME', 6:'DNS_SOA', 10:'DNS_NULL', 12:'DNS_PTR', 13:'DNS_HINFO',
                            15:'DNS_MX', 16:'DNS_TXT', 28:'DNS_AAAA', 33:'DNS_SRV', 41:'DNS_OPT'}

        # Query classes
        self.query_classes = {1:'DNS_IN', 3:'DNS_CHAOS', 4:'DNS_HESIOD', 254:'DNS_NONE', 255:'DNS_ANY'}

    def dns_meta_data(self):
        """Pull out the dns metadata for packet/transport in the input_stream"""

        # For each packet process the contents
        for packet in self.input_stream:
            # Skip packets without transport info (ARP/ICMP/IGMP/whatever)
            if 'transport' not in packet:
                continue
            try:
                dns_meta = dpkt.dns.DNS(packet['transport']['data'])
                _raw_info = data_utils.make_dict(dns_meta)
                packet['dns'] = self._dns_info_mapper(_raw_info)
                packet['dns']['_raw'] = _raw_info
            except (dpkt.dpkt.NeedData, dpkt.dpkt.UnpackError):
                if 'dns' in packet:
                    del packet['dns']

            # All done
            yield packet

    def _dns_info_mapper(self, raw_dns):
        """The method maps the specific fields/flags in a DNS record to human readable form"""
        output = {}

        # Indentification
        output['identification'] = raw_dns['id']

        # Pull out all the flags
        flags = {}
        flags['type'] = 'query' if raw_dns['qr'] == 0 else 'response'
        flags['opcode'] = self.opcodes.get(raw_dns['opcode'], 'UNKNOWN')
        flags['authoritative'] = True if raw_dns['aa'] else False
        flags['truncated'] = True if raw_dns['tc'] else False
        flags['recursion_desired'] = True if raw_dns['rd'] else False
        flags['recursion_available'] = True if raw_dns['ra'] else False
        flags['zero'] = raw_dns['zero']
        flags['return_code'] = self.rcodes.get(raw_dns['rcode'], 'UNKNOWN')
        output['flags'] = flags

        # Question/Answer Counts
        counts = {}
        counts['questions'] = len(raw_dns['qd'])
        counts['answers'] = len(raw_dns['an'])
        counts['auth_answers'] = len(raw_dns['ns'])
        counts['add_answers'] = len(raw_dns['ar'])
        output['counts'] = counts

        # Queries/Questions
        queries = []
        for query in raw_dns['qd']:
            q = {'class': self.query_classes.get(query['cls'], 'UNKNOWN'),
                 'type': self.query_types.get(query['type'], 'UNKNOWN'),
                 'name': query['name'],
                 'data': query['data']}
            queries.append(q)
        output['queries'] = queries


        # Responses/Answers (Resource Record)
        output['answers'] = {}
        for section_name, section in zip(['answers', 'name_servers', 'additional'], ['an', 'ns', 'ar']):
            answers = []
            for answer in raw_dns[section]:
                ans_output = {}
                ans_output['name'] = answer['name']
                ans_output['type'] = self.query_types.get(answer['type'], 'UNKNOWN')
                ans_output['class'] = self.query_classes.get(answer['cls'], 'UNKNOWN')
                ans_output['ttl'] = answer['ttl']

                # Get the return data for this answer type
                rdata_field = self._get_rdata_field(answer)
                if rdata_field != 'unknown':
                    ans_output['rdata'] = answer[rdata_field]
                answers.append(ans_output)

            # Add data to this answer section
            output['answers'][section_name] = answers

        # Add any weird stuff
        weird = self._dns_weird(output)
        if weird:
            output['weird'] = weird

        return output

    def _dns_weird(self, record):
        """Look for weird stuff in dns record using a set of criteria to mark the weird stuff"""
        weird = {}

        # Zero should always be 0
        if record['flags']['zero'] != 0:
            weird['zero'] = record['flags']['zero']

        # Trucated may indicate an exfil
        if record['flags']['truncated']:
            weird['trucnated'] = True

        # Weird Query Types
        weird_types = set(['DNS_NULL', 'DNS_HINFO', 'DNS_TXT', 'UNKNOWN'])
        for query in record['queries']:
            if query['type'] in weird_types:
                weird['query_type'] = query['type']

        # Weird Query Classes
        weird_classes = set(['DNS_CHAOS', 'DNS_HESIOD', 'DNS_NONE', 'DNS_ANY'])
        for query in record['queries']:
            if query['class'] in weird_classes:
                weird['query_class'] = query['class']

        # Weird Answer Types
        for section_name in ['answers', 'name_servers', 'additional']:
            for answer in record['answers'][section_name]:
                if answer['type'] in weird_types:
                    weird['answer_type'] = answer['type']

        # Weird Answer Classes
        for section_name in ['answers', 'name_servers', 'additional']:
            for answer in record['answers'][section_name]:
                if answer['class'] in weird_classes:
                    weird['answer_class'] = answer['class']

        # Is the subdomain name especially long or have high entropy?
        for query in record['queries']:
            subdomain = '.'.join(query['name'].split('.')[:-2])
            length = len(subdomain)
            entropy = self.entropy(subdomain)
            if length > 35 and entropy > 3.5:
                weird['subdomain_length'] = length
                weird['subdomain'] = subdomain
                weird['subdomain_entropy'] = entropy
                weird['subdomain'] = subdomain

        # Return the weird stuff
        return weird


    @staticmethod
    def entropy(string):
        """Compute entropy on the string"""
        p, lns = Counter(string), float(len(string))
        return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

    @staticmethod
    def _get_rdata_field(answer):
        """Helper method to find the rdata field for various answer types"""
        for field in ['mxname', 'nsname', 'cname', 'text', 'rname', 'null', 'ptrname']:
            if field in answer:
                return field
        return 'unknown'

def test():
    """Test for DNSMeta class"""
    import pprint

    # Local imports
    from chains.sources import packet_streamer
    from chains.links import packet_meta, reverse_dns, transport_meta

    # Create a PacketStreamer, a PacketMeta, and link them to DNSMeta
    data_path = file_utils.relative_dir(__file__, '../../data/dns.pcap')
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10000)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = transport_meta.TransportMeta()
    dns_meta = DNSMeta()

    # Set up chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)
    dns_meta.link(tmeta)

    # Print out the DNS meta data
    for item in dns_meta.output_stream:
        if 'dns' in item:
            print()
            pprint.pprint(item['dns'])
        else:
            print('.', end='')

if __name__ == '__main__':
    test()
