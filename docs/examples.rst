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

**Code from examples/simple_packet_print.py**

.. code-block:: python

    # Create the classes
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    printer = packet_printer.PacketPrinter()

    # Set up the chain
    meta.input_stream = streamer.output_stream
    printer.input_stream = meta.output_stream

    # Pull the chain
    printer.pull()


**Example Output**

.. code-block:: json

    Timestamp: 2015-05-24 04:19:03.071789
    Ethernet Frame: 6c:40:08:89:fc:08 --> b0:ee:45:49:7b:81  (type: 2048)
    IP: 192.168.1.9 --> 192.168.1.3 (len:52 ttl:64) -- Frag(df:1 mf:0 offset:0)

    Timestamp: 2015-05-24 04:19:03.072032
    Ethernet Frame: b0:ee:45:49:7b:81 --> 6c:40:08:89:fc:08  (type: 2048)
    IP: 192.168.1.3 --> 192.168.1.9 (len:163 ttl:64) -- Frag(df:1 mf:0 offset:0)

    Timestamp: 2015-05-24 04:19:03.072097
    Ethernet Frame: 6c:40:08:89:fc:08 --> b0:ee:45:49:7b:81  (type: 2048)
    IP: 192.168.1.9 --> 192.168.1.3 (len:52 ttl:64) -- Frag(df:1 mf:0 offset:0)


Example Reference
=================
.. automodule:: examples.simple_packet_print

