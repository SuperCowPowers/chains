========
Examples
========
We present a set of examples that hopefully show how you can use Chains to build
flexible pipelines of streaming data.

Lets Print some Packets 
=======================
Printing packets is about the simplest chain you could have. It takes a PacketStreamer()
source, a PacketMeta() link, and a PacketPrinter() sink. It links those together in a chain
(see what I did there) and prints out the packets. 

**See these classes**

.. autosummary:: chains.sources.packet_streamer
.. autosummary:: chains.links.packet_meta
.. autosummary:: chains.sinks.packet_printer

**Code**

.. code-block:: python

    # Import the classes we want
    from chains.sources import packet_streamer
    from chains.links import packet_meta
    from chains.utils import file_utils

    # Create the classes
    streamer = packet_streamer.PacketStreamer()
    meta = packet_meta.PacketMeta()
    printer = PacketPrinter()

    # Set up the chain
    meta.input_stream = streamer.output_stream
    printer.input_stream = meta.output_stream

    # Pull the chain
    printer.pull()


**Example Output**

.. code-block:: json

    Timestamp:  2015-05-22 20:45:35.907100
    Ethernet Frame:  e4:f4:c6:06:b2:8d 6c:40:08:89:fc:08 2048
    IP: 12.226.156.82 -> 192.168.1.9   (len=494 ttl=52 DF=1 MF=0 offset=0)

    Timestamp:  2015-05-22 20:45:35.907155
    Ethernet Frame:  6c:40:08:89:fc:08 e4:f4:c6:06:b2:8d 2048
    IP: 192.168.1.9 -> 12.226.156.82   (len=52 ttl=64 DF=1 MF=0 offset=0)

    Timestamp:  2015-05-22 20:45:35.907290
    Ethernet Frame:  6c:40:08:89:fc:08 e4:f4:c6:06:b2:8d 2048
    IP: 192.168.1.9 -> 12.226.156.82   (len=190 ttl=64 DF=1 MF=0 offset=0)

