#!/usr/bin/env python
"""
    Source Class
"""

# Local imports
from chains.links import link
from chains.utils import log_utils
log_utils.log_defaults()

class Source(link.Link):
    """Sources provide an output_stream but do not take in input stream"""
    def __init__(self):
        """Initialize Source Class"""

        # Call super class init
        super(Source, self).__init__()        

    @property
    def input_stream(self):
        """The input stream property (not provided for a source)"""
        log_utils.panic_and_throw('Sources do not provice input streams')

    @input_stream.setter
    def input_stream(self, input_stream):
        """Set the input stream (not provided for a source)"""
        log_utils.panic_and_throw('Sources do not provice input streams')

def test():
    """Spin up the source class and call the methods"""
    link = Source()

    # This will both raise a RuntimeError (source don't provide input_streams)
    try:
        link.input_stream
    except RuntimeError:
        pass
    try:
        link.input_stream = [{'foo':5}, {'foo':8}]
    except RuntimeError:
        pass

if __name__ == '__main__':
    test()
