Chains
======

.. include:: badges.rst

The Chains project is an exploration of python components that you 
'chain' together to process streaming network packets. The use of
native python generators means the code is extremely lightweight and 
efficient.


Install/Run Stuff
-----------------
Want to see what's happening on your network right now? Just install chains and run 'netwatch'.
::

    $ pip install chains
    $ netwatch -s
    2015-09-07 19:08:34 - UDP IP 192.168.1.9(internal)--> 224.0.0.251(multicast_dns)
    2015-09-07 19:08:34 - UDP IP6 fe80::6e40:8ff:fe89:fc08(internal)--> ff02::fb(multicast_dns)
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
   Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36

   HTTP_REQUEST
   192.168.1.9 --> Host: ajax.googleapis.com
   URI: /ajax/libs/jquery/1.7.1/jquery.min.js
   Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36

   HTTPS_REQUEST
   192.168.1.9 --> 199.166.0.200(sc.iasds01.com) tls_records(5)
   TLSRecord(length=512, version=769, type=22, data='\x01\x00\x01\xfc\x03\x03K\t\xf8_\x8...
   TLSRecord(length=560, version=771, type=23, data='\x1d\x942K\xfb\x87\x19v\xba\x13\x14...
   ...

Examples and References
-----------------------
.. toctree::
    :maxdepth: 3

    examples

.. toctree::
    :maxdepth: 3

    class_reference/index

Help the Project
----------------
.. toctree::
    :maxdepth: 2

    contributing

Indices and tables
------------------
 
 * :ref:`genindex`
 * :ref:`modindex`
