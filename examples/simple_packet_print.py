""" Example: Simple Packet Printer """

# Local imports
from chains.sources import packet_streamer
from chains.links import packet_meta
from chains.sinks import packet_printer

def run(iface_name=None, max_packets=100):
    """Run the Simple Packet Printer Example"""

    # Create the classes
    streamer = packet_streamer.PacketStreamer(iface_name=iface_name, max_packets=max_packets)
    meta = packet_meta.PacketMeta()
    printer = packet_printer.PacketPrinter()

    # Set up the chain
    meta.input_stream = streamer.output_stream
    printer.input_stream = meta.output_stream

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
    run()
