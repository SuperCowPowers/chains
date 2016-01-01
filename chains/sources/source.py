"""
   Sources provide an output_stream but do not take in input stream,
"""

# Local imports
from chains.links import link
from chains.utils import log_utils
log_utils.get_logger()

class Source(link.Link):
    """Sources provide an output_stream but do not take in input stream"""
    def __init__(self):
        """Initialize Source Class"""

        # Call super class init
        super(Source, self).__init__()

    @property
    def input_stream(self):
        """The input stream property (not provided for a source)"""
        log_utils.panic('Sources do not provice input streams')


def test():
    """Spin up the source class and call the methods"""
    source = Source()

    # This will both raise a RuntimeError (source don't provide input_streams)
    try:
        source.input_stream
    except RuntimeError:
        pass

if __name__ == '__main__':
    test()
