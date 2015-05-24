"""
   Links take an input_stream and provides an output_stream. 
   All streams are enforced to a generator that yields python dictionaries.
"""

# Local imports
from chains.utils import log_utils
log_utils.log_defaults()

class Link(object):
    """Links take an input_stream and provides an output_stream. All streams
       are enforced to a generator that yields python dictionaries.
    """
    def __init__(self):
        """Initialize Link Class"""
        self._input_stream = None
        self._output_stream = None
    
        # Call super class init
        super(Link, self).__init__()

    @property
    def input_stream(self):
        """The input stream property"""
        if not self._input_stream:
            log_utils.panic_and_throw('No input stream set yet!')
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
    link = Link()

    # This will raise a RuntimeError (because we haven't set it yet)
    try:
        link.input_stream
    except RuntimeError:
        pass
    link.input_stream = [{'foo':5}, {'foo':8}]
    assert link.input_stream
    assert link.output_stream == None


if __name__ == '__main__':
    test()
