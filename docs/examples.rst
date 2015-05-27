========
Examples
========
We present a set of examples that hopefully show how you can use Chains to build
flexible pipelines of streaming data.

Lets Print some Packets 
=======================
Printing packets is about the simplest chain you could have. It takes a 

- PacketStreamer() :py:class:`chains.sources.packet_streamer`
- PacketMeta() :py:class:`chains.links.packet_meta`
- ReverseDNS() :py:class:`chains.links.reverse_dns`
- PacketPrinter() :py:class:`chains.sinks.packet_printer`

We link these together in a chain (see what I did there) and we pull the chain.
Pulling the chain will stream data from one component to another which only uses
the memory required to hold one packet. You could literally run this all day every 
day for a year on your home network and never run out of memory.

**Code from examples/simple_packet_print.py**

.. code-block:: python

    # Create the classes
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=10)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    printer = packet_printer.PacketPrinter()

    # Set up the chain
    meta.link(streamer)
    rdns.link(meta)
    printer.link(rdns)

    # Pull the chain
    printer.pull()


**Example Output**

.. code-block:: json

    Timestamp: 2015-05-27 01:17:07.919743
    Ethernet Frame: 6c:40:08:89:fc:08 --> 01:00:5e:00:00:fb  (type: 2048)
    Packet: IP 192.168.1.9 --> 224.0.0.251 (len:55 ttl:255) -- Frag(df:0 mf:0 offset:0)
    Domains: LOCAL --> multicast_dns
    Transport: UDP {'dport': 5353, 'sum': 59346, 'sport': 5353, 'data': '\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03CTV\x05local\x00\x00\x1c\x80\x01', 'ulen': 35}
    Application: None
    
    Timestamp: 2015-05-27 01:17:07.919926
    Ethernet Frame: 6c:40:08:89:fc:08 --> 33:33:00:00:00:fb  (type: 34525)
    Packet: IP6 fe80::6e40:8ff:fe89:fc08 --> ff02::fb (len:35 ttl:255)
    Domains: LOCAL --> multicast_dns
    Transport: UDP {'dport': 5353, 'sum': 6703, 'sport': 5353, 'data': '\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03CTV\x05local\x00\x00\x1c\x80\x01', 'ulen': 35}
    Application: None
    
    ...


Example Reference
=================
.. automodule:: examples.simple_packet_print

