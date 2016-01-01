"""
   Sinks take an input_stream and provides a pull() method.
   Note: Sinks do not provide an output_stream.
"""

# Local imports
from chains.links import link
from chains.utils import log_utils
log_utils.get_logger()

class Sink(link.Link):
    """Sinks take an input_stream and provides a pull() method
       Note: Sinks do not provide an output_stream.
    """
    def __init__(self):
        """Initialize Sink Class"""

        # Call super class init
        super(Sink, self).__init__()

    @property
    def output_stream(self):
        """The output stream property"""
        log_utils.panic('Sinks do not provice output streams')

    def pull(self):
        """Process the input stream"""
        raise NotImplementedError("Please Implement this method")

def test():
    """Spin up the sink class and call the methods"""
    link = Sink()

    # This will raise a RuntimeError (because sinks don't provide output streams)
    try:
        link.output_stream
    except RuntimeError:
        pass

if __name__ == '__main__':
    test()
