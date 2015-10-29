#!/usr/bin/env python
""" Example: Simple Packet Printer """
import os
import argparse

# Local imports
from chains.utils import signal_utils
from chains.sources import packet_streamer
from chains.links import packet_meta, reverse_dns, transport_meta
from chains.sinks import packet_printer, packet_summary

def run(iface_name=None, bpf=None, summary=None, max_packets=100):
    """Run the Simple Packet Printer Example"""

    # Create the classes
    streamer = packet_streamer.PacketStreamer(iface_name=iface_name, bpf=bpf, max_packets=max_packets)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    tmeta = transport_meta.TransportMeta()
    if summary:
        printer = packet_summary.PacketSummary()
    else:
        printer = packet_printer.PacketPrinter()

    # Set up the chain
    meta.link(streamer)
    rdns.link(meta)
    tmeta.link(rdns)
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

def my_exit():
    """Exit on Signal"""
    print 'Goodbye...'

if __name__ == '__main__':

    # Collect args from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-bpf', type=str, help='BPF Filter for PacketStream Class')
    parser.add_argument('-s','--summary', action="store_true", help='Summary instead of full packet print')
    parser.add_argument('-m','--max-packets', type=int, default=100, help='How many packets to process (0 for infinity)')
    parser.add_argument('-p','--pcap', type=str, help='Specify a pcap file instead of reading from live network interface')
    args, commands = parser.parse_known_args()
    if commands:
        print 'Unrecognized args: %s' % commands
    try:
        # Pcap file may have a tilde in it
        if args.pcap:
            args.pcap = os.path.expanduser(args.pcap)

        with signal_utils.signal_catcher(my_exit):
            run(iface_name=args.pcap, bpf=args.bpf, summary=args.summary, max_packets=args.max_packets)
    except KeyboardInterrupt:
        print 'Goodbye...'
