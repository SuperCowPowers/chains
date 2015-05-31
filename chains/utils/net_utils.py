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
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, address)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, address)

def is_internal(ip_address):
    """Determine if the address is an internal ip address
       Note: This is super bad, improve it
    """
    # Local networks 10.0.0.0/8, 172.16.0.0/12, '192.168.0.0/16
    local_nets = '10.', '172.16.', '192.168.', '169.254', 'fd', 'fe80::'
    return any([ip_address.startswith(local) for local in local_nets])

def is_special(ip_address):
    """Determine if the address is SPECIAL
       Note: This is super bad, improve it
    """
    special = {'224.0.0.251': 'multicast_dns',
               'ff02::fb': 'multicast_dns'}
    return special[ip_address] if ip_address in special else None

def test_utils():
    """Test the utility methods"""
    print mac_addr('\x00\x00\x01\x00\x00\x00')
    print ip_to_str('\x91\xfe\xa0\xed')
    print 'Success!'

if __name__ == '__main__':
    test_utils()
