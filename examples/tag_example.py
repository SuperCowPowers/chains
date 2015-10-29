""" Example: Simple Tagger """
import argparse

# Local imports
from chains.sources import packet_streamer
from chains.links import packet_meta, reverse_dns, packet_tags, transport_meta
from chains.sinks import packet_printer
from chains.sinks import packet_summary

def run(iface_name=None, bpf=None, summary=None, max_packets=50):
    """Run the Simple Packet Printer Example"""

    # Create the classes
    streamer = packet_streamer.PacketStreamer(iface_name=iface_name, bpf=bpf, max_packets=max_packets)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tags = packet_tags.PacketTags() 
    tmeta = transport_meta.TransportMeta()
    printer = packet_summary.PacketSummary()

    # Set up the chain
    meta.link(streamer)
    rdns.link(meta)
    tags.link(rdns)
    tmeta.link(tags)
    printer.link(tmeta)

    # Pull the chain
    printer.pull()

def test():
    """Test the Simple Packet Printer Example"""
    from chains.utils import file_utils

    # For the test we grab a file, but if you don't specify a
    # it will grab from the first active interface
    data_path = file_utils.relative_dir(__file__, '../data/http.pcap')
    run(iface_name = data_path)

if __name__ == '__main__':

    # Collect args from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-bpf', type=str, help='BPF Filter for PacketStream Class')
    parser.add_argument('-m','--max-packets', type=int, default=50, help='How many packets to process (0 for infinity)')
    args, commands = parser.parse_known_args()
    try:
        run(bpf=args.bpf, max_packets=args.max_packets)
    except KeyboardInterrupt:
        print 'Goodbye...'
