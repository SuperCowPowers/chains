Chains
======

**Python Chained Generators for Network Packets:** `Read the
Docs <http://chains.rtfd.org>`__

|travis| |Coverage Status| |landscape| |version| |downloads|

|wheel| |supported-versions| |supported-implementations| |gitter|

Installation
------------

::

    pip install py-chains

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
.. |version| image:: https://img.shields.io/pypi/v/py-chains.svg
   :target: https://pypi.python.org/pypi/py-chains
.. |downloads| image:: https://img.shields.io/pypi/dm/py-chains.svg
   :target: https://pypi.python.org/pypi/py-chains
.. |wheel| image:: https://img.shields.io/pypi/wheel/py-chains.svg
   :target: https://pypi.python.org/pypi/py-chains
.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/py-chains.svg
   :target: https://pypi.python.org/pypi/py-chains
.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/py-chains.svg
   :target: https://pypi.python.org/pypi/py-chains
.. |gitter| image:: https://badges.gitter.im/Chat.svg
   :target: https://gitter.im/SuperCowPowers/chains?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
