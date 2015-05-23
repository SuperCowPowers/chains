========
Examples
========
We present a set of examples that hopefully show how you can use Chains to build
flexible pipelines of streaming data.

print_packets.py
================
Print packets is about the simplest chain you could have. It takes a stream_packet
source and prints out the packets. It's a 'sink' meaning that it
cannot be an input into another chain. 

stream_packets -> print_packet

.. automodule:: chains.print_packets

**Code Excerpt**

.. code-block:: python

    """Get a packet stream source and give it to print_packets :) """
    packet_stream = stream_packets.stream_packets(max_packets=10)
    print_packets(packet_stream)


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

