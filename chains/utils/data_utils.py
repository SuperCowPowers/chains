"""Data utilities that might be useful"""

from __future__ import print_function

# Local imports
from chains.utils import log_utils

def make_dict(obj):
    """This method creates a dictionary out of a non-builtin object"""

    # Recursion base case
    if is_builtin(obj):
        return obj

    output_dict = {}
    for key in dir(obj):
        if not key.startswith('__') and not callable(getattr(obj, key)):
            attr = getattr(obj, key)
            if isinstance(attr, list):
                output_dict[key] = []
                for item in attr:
                    output_dict[key].append(make_dict(item))
            else:
                output_dict[key] = make_dict(attr)

    # All done
    return output_dict

def is_builtin(obj):
    return obj.__class__.__module__ in ['__builtin__', 'builtins']

def get_value(data, key):
    """Follow the dot notation to get the proper field, then perform the action

       Args:
           data: the data as a dictionary (required to be a dictionary)
           key: the key (as dot notation) into the data that gives the field (IP.src)

        Returns:
           the value of the field(subfield) if it exist, otherwise None
    """
    ref = data
    try:
        for subkey in key.split('.'):
            if isinstance(ref, dict):
                ref = ref[subkey]
            else:
                print('CRITICAL: Cannot use subkey %s on non-dictionary element' % subkey)
                return None
        return ref

    # In general KeyErrors are expected
    except KeyError:
        return None

def test_utils():
    """Test the utility methods"""
    good = {'IP':{'src':'123'}}
    bad = {'IP':{'srrcc':'123'}}
    bad2 = {'IP':['src','123']}
    assert get_value(good, 'IP.src')
    assert get_value(bad, 'IP.src') == None
    assert get_value(bad2, 'IP.src') == None

    class bla(object):
        def func_foo(self):
            pass
    bla.a = 'foo'
    bla.b = 'bar'
    print(make_dict(bla))
    print('Success!')

if __name__ == '__main__':
    test_utils()
