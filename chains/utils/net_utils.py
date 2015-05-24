"""Network utilities that might be useful"""
import socket

def mac_addr(mac_string):
    """Print out MAC address given a string

       Args:
           mac_string: the string representation of a MAC address
       Returns:
           printable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in mac_string)

def ip_to_str(address):
    """Print out an IP address given a string

       Args:
           address: the string representation of a MAC address
       Returns:
           printable IP address
    """
    return socket.inet_ntop(socket.AF_INET, address)

def test_utils():
    """Test the utility methods"""
    print mac_addr('\x00\x00\x01\x00\x00\x00')
    print ip_to_str('\x91\xfe\xa0\xed')
    print 'Success!'

if __name__ == '__main__':
    test_utils()
