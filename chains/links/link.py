"""
   Links take an input_stream and provides an output_stream. 
   All streams are enforced to a generator that yields python dictionaries.
"""

# Local imports
from chains.utils import log_utils
log_utils.log_defaults()

class Link(object):
    """Link classes take an input_stream and provide an output_stream. All streams
       are expected to be a generator that yields python dictionaries.
    """
    def __init__(self):
        """Initialize Link Class"""
        self._input_stream = None
        self._output_stream = None
    
        # Call super class init
        super(Link, self).__init__()

    def link(self, stream_object):
        """Set my input stream"""
        self.input_stream = stream_object.output_stream

    @property
    def input_stream(self):
        """The input stream property"""
        return self._input_stream

    @input_stream.setter
    def input_stream(self, input_stream):
        """Set the input stream

           Args:
               input_stream: a generator that yields dictionaries
        """
        if not input_stream:
            log_utils.panic_and_throw('The input stream is None!')        
        self._input_stream = input_stream

    @property
    def output_stream(self):
        """The output stream property"""
        return self._output_stream

def test():
    """Spin up the link class and call the methods"""

    # Create a couple of dummy classes
    link1 = Link()
    link1._output_stream = [{'foo':5, 'bar':3}] # Just for testing
    link2 = Link()
    link2.link(link1)
    print link2.input_stream


if __name__ == '__main__':
    test()
