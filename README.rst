Chains
======

**Python Chained Generators for Network Packets:** `Read the
Docs <http://chains.rtfd.org>`__

|travis| |Coverage Status| |landscape| |version| |downloads| 
|wheel| |supported-versions| |supported-implementations| |gitter|

Install/Run Stuff
-----------------
Want to see what's happening on your network right now? Just install chains and run 'netwatch'.
::

    $ pip install chains
    $ netwatch -s
    2015-09-07 19:08:34 - UDP IP 192.168.1.9(internal)--> 224.0.0.251(multicast_dns)
    2015-09-07 19:08:34 - UDP IP6 fe80::6e40:8ff:fe89:fc08(internal) --> ff02::fb(multicast_dns)
    2015-09-07 19:08:34 - UDP IP 192.168.1.14(internal)--> 224.0.0.251(multicast_dns)
    2015-09-07 19:08:34 - UDP IP6 fe80::8a0:4946:3c8a:e6a1(internal)--> ff02::fb(multicast_dns)
    2015-09-07 19:08:34 - TCP IP 192.168.1.9(internal)--> 49.75.183.151(nxdomain)
    2015-09-07 19:08:36 - TCP IP 192.168.1.9(internal)--> 54.164.252.174(compute-1.amazonaws.com)
    2015-09-07 19:08:36 - UDP IP 192.168.1.1(internal)--> 192.168.1.9(internal)
    2015-09-07 19:08:36 - TCP IP 54.164.252.174(compute-1.amazonaws.com)--> 192.168.1.9(internal)
    ...

Want to go to coffee shop and see http(s) requests floating about?
::

   $ urlwatch

   HTTP_REQUEST
   192.168.1.9 --> Host: clc.stackoverflow.com
   URI: /j/p.js?d=hireme&ac=891012&tags=python;attributes&lw=5913&bw=1539
   Referer: http://stackoverflow.com/questions/610883/attribute-in-python
   Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36

   HTTP_REQUEST
   192.168.1.9 --> Host: ajax.googleapis.com
   URI: /ajax/libs/jquery/1.7.1/jquery.min.js
   Referer: http://stackoverflow.com/questions/610883/attribute-in-python
   Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36

   HTTPS_REQUEST
   192.168.1.9 --> 199.166.0.200(sc.iasds01.com) tls_records(5)
   TLSRecord(length=512, version=769, type=22, data='\x01\x00\x01\xfc\x03\x03K\t\xf8_\x8...
   TLSRecord(length=262, version=771, type=22, data='\x10\x00\x01\x02\x01\x00Vfd\x8f8a\x...
   TLSRecord(length=1, version=771, type=20, data='\x01')
   TLSRecord(length=64, version=771, type=22, data="l\xd0\xce\x96\xf5\x1a\xf8\xcf\xcc\x1...
   TLSRecord(length=560, version=771, type=23, data='\x1d\x942K\xfb\x87\x19v\xba\x13\x14...

Documentation
-------------

`chains.readthedocs.org <https://chains.readthedocs.org/>`__

About
-----

The Chains project is an exploration of python components that you
'chain' together to process streaming network packets. The use of
native python generators means the code is extremely lightweight and
efficient.

Example
-------

::

    # Create the classes
    streamer = packet_streamer.PacketStreamer(iface_name=data_path, max_packets=50)
    meta = packet_meta.PacketMeta()
    rdns = reverse_dns.ReverseDNS()
    printer = packet_printer.PacketPrinter()

    # Set up the chain
    meta.link(streamer)
    rdns.link(meta)
    printer.link(rdns)

    # Pull the chain
    printer.pull()

Example Output
~~~~~~~~~~~~~~

::

    Timestamp: 2015-05-27 01:17:07.919743
    Ethernet Frame: 6c:40:08:89:fc:08 --> 01:00:5e:00:00:fb  (type: 2048)
    Packet: IP 192.168.1.9 --> 224.0.0.251 (len:55 ttl:255) -- Frag(df:0 mf:0 offset:0)
    Domains: LOCAL --> multicast_dns
    Transport: UDP {'dport': 5353, 'sum': 59346, 'sport': 5353, 'data': '...', 'ulen': 35}
    Application: None

    Timestamp: 2015-05-27 01:17:07.919926
    Ethernet Frame: 6c:40:08:89:fc:08 --> 33:33:00:00:00:fb  (type: 34525)
    Packet: IP6 fe80::6e40:8ff:fe89:fc08 --> ff02::fb (len:35 ttl:255)
    Domains: LOCAL --> multicast_dns
    Transport: UDP {'dport': 5353, 'sum': 6703, 'sport': 5353, 'data': '...', 'ulen': 35}
    Application: None
    ...

LICENSE
-------

MIT Licensed

.. |travis| image:: https://img.shields.io/travis/SuperCowPowers/chains.svg
   :target: https://travis-ci.org/SuperCowPowers/chains
.. |Coverage Status| image:: https://coveralls.io/repos/SuperCowPowers/chains/badge.svg?branch=HEAD
   :target: https://coveralls.io/r/SuperCowPowers/chains
.. |landscape| image:: https://landscape.io/github/SuperCowPowers/chains/master/landscape.svg?style=flat
   :target: https://landscape.io/github/SuperCowPowers/chains/master
.. |version| image:: https://img.shields.io/pypi/v/chains.svg
   :target: https://pypi.python.org/pypi/chains
.. |downloads| image:: https://img.shields.io/pypi/dm/chains.svg
   :target: https://pypi.python.org/pypi/chains
.. |wheel| image:: https://img.shields.io/pypi/wheel/chains.svg
   :target: https://pypi.python.org/pypi/chains
.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/chains.svg
   :target: https://pypi.python.org/pypi/chains
.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/chains.svg
   :target: https://pypi.python.org/pypi/chains
.. |gitter| image:: https://badges.gitter.im/Chat.svg
   :target: https://gitter.im/SuperCowPowers/chains?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
