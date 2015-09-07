Chains
======

.. include:: badges.rst

The Chains project is an exploration of python components that you 
'chain' together to process streaming network packets. The use of
native python generators means the code is extremely lightweight and 
efficient.


Install/Run Stuff
-----------------
Want to see what's happening on your network right now? Just install chains and run 'net_watch'.
::

    $ pip install chains
    $ net_watch -s
    2015-09-07 19:08:34 - UDP IP 192.168.1.9(internal) --> 224.0.0.251(multicast_dns)
    2015-09-07 19:08:34 - UDP IP6 fe80::6e40:8ff:fe89:fc08(internal) --> ff02::fb(multicast_dns)
    2015-09-07 19:08:34 - UDP IP 192.168.1.14(internal) --> 224.0.0.251(multicast_dns)
    2015-09-07 19:08:34 - UDP IP6 fe80::8a0:4946:3c8a:e6a1(internal) --> ff02::fb(multicast_dns)
    2015-09-07 19:08:34 - TCP IP 192.168.1.9(internal) --> 49.75.183.151(nxdomain)
    2015-09-07 19:08:36 - TCP IP 192.168.1.9(internal) --> 54.164.252.174(ec2-54-164-252-174.compute-1.amazonaws.com)
    2015-09-07 19:08:36 - UDP IP 192.168.1.1(internal) --> 192.168.1.9(internal)
    2015-09-07 19:08:36 - TCP IP 54.164.252.174(ec2-54-164-252-174.compute-1.amazonaws.com) --> 192.168.1.9(internal)
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
