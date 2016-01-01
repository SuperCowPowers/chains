"""
   Links take an input_stream and provides an output_stream. All streams
   are required to be a generator that yields python dictionaries.
"""
import collections

# Local imports
from chains.utils import log_utils
log_utils.get_logger()

class Link(object):
    """Link classes take an input_stream and provide an output_stream. All streams
       are required to be a generator that yields python dictionaries.
    """
    def __init__(self):
        """Initialize Link Class"""
        self._input_stream = None
        self._output_stream = None

    def link(self, stream_instance):
        """Set my input stream"""
        if isinstance(stream_instance, collections.Iterable):
            self.input_stream = stream_instance
        elif getattr(stream_instance, 'output_stream', None):
            self.input_stream = stream_instance.output_stream
        else:
            raise RuntimeError('Calling link() with unknown instance type %s' % type(stream_instance))

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
            log_utils.panic('The input stream is None!')
        self._input_stream = input_stream

    @property
    def output_stream(self):
        """The output stream property"""
        return self._output_stream

    @output_stream.setter
    def output_stream(self, output_stream):
        """Set the output stream

           Args:
               output_stream: a generator that yields dictionaries
        """
        if not output_stream:
            log_utils.panic('The output stream is None!')
        self._output_stream = output_stream

def test():
    """Spin up the link class and call the methods"""

    # Create a couple of dummy classes
    link1 = Link()
    link1.output_stream = [{'foo':5, 'bar':3}] # Just for testing
    link2 = Link()
    link2.link(link1)
    print link2.input_stream


if __name__ == '__main__':
    test()
