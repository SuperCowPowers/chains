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

    Timestamp: 2015-05-25 01:42:41.430436
    Ethernet Frame: 6c:40:08:89:fc:08 --> e4:f4:c6:06:b2:8d  (type: 2048)
    Packet: IP 192.168.1.9 --> 157.55.56.170 (len:52 ttl:64) -- Frag(df:1 mf:0 offset:0)
    Transport: TCP {'off': 8, 'seq': 491703910, 'off_x2': 128, 'ack': 82501583, 'win': 3931, 
                   'sum': 32580, 'flags': 16, 'dport': 40032, 'urp': 0, 'sport': 54247,
                   'data': '', 'opts': '\x01\x01\x08\n:\xc4tbU\xa6\x0b\x07'}
    Application: None
    
    Timestamp: 2015-05-25 01:42:41.449987
    Ethernet Frame: e4:f4:c6:06:b2:8d --> 6c:40:08:89:fc:08  (type: 2048)
    Packet: IP 157.55.130.143 --> 192.168.1.9 (len:48 ttl:51) -- Frag(df:1 mf:0 offset:0)
    Transport: UDP {'dport': 17887, 'sum': 9425, 'sport': 40008, 
                    'data': '|\x9a\x02b\x17\x1c\xc07\xd0\xff\x11\xd3:3X\x01\x93\x16\xb8\xd6', 'ulen': 28}
    Application: None
    
    ...


Example Reference
=================
.. automodule:: examples.simple_packet_print

