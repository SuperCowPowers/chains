===============
Class Reference
===============
The Chains packets is split into following sub-packages

* Sources: Classes with produce data (they have an output_stream but NOT an input_stream)
* Links: Classes that consume an input_stream and produce an output_stream
* Sinks: Classes that consume an input_stream but do NOT produce an output_stream
* Utils: Helpful utility methods (HHAC/IP to str, file helpers, log utils)

.. toctree::
     :maxdepth: 3

     sources

.. toctree::
     :maxdepth: 3

     links

.. toctree::
     :maxdepth: 3

     sinks

.. toctree::
     :maxdepth: 3

     utils
