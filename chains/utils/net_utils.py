"""Network utilities that might be useful"""
import socket
import json
import binascii
import netifaces

# Local imports
from chains.utils import file_utils

def get_default_interface():
    """Grab the name of the local default network interface"""
    return netifaces.gateways()['default'][netifaces.AF_INET][1]

def get_ip_address(iface_name):
    """Get the ip address of the named network interface"""
    return netifaces.ifaddresses(iface_name)[netifaces.AF_INET][0]['addr']

def get_mac_address(iface_name):
    """Get the mac address of the named network interface"""
    return netifaces.ifaddresses(iface_name)[netifaces.AF_LINK][0]['addr']

def get_broadcast_address(iface_name):
    """Get the broadcast address of the named network interface"""
    return netifaces.ifaddresses(iface_name)[netifaces.AF_INET][0]['broadcast']

def mac_to_str(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in address)

def str_to_mac(mac_string):
    """Convert a readable string to a MAC address

           Args:
               mac_string (str): a readable string (e.g. '01:02:03:04:05:06')
           Returns:
               str: a MAC address in hex form
        """
    sp = mac_string.split(':')
    mac_string = ''.join(sp)
    return binascii.unhexlify(mac_string)

def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def str_to_inet(address):
    """Convert an a string IP address to a inet struct

        Args:
            address (str): String representation of address
        Returns:
            inet: Inet network address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_pton(socket.AF_INET, address)
    except socket.error:
        return socket.inet_pton(socket.AF_INET6, address)

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
    return special[ip_address] if ip_address in special else False

def test_utils():
    """Test the utility methods"""
    print mac_to_str('\x01\x02\x03\x04\x05\x06')
    assert mac_to_str('\x01\x02\x03\x04\x05\x06') == '01:02:03:04:05:06'
    assert str_to_mac('01:02:03:04:05:06') == '\x01\x02\x03\x04\x05\x06'
    foo = '\x01\x02\x03\x04\x05\x06'
    bar = mac_to_str(foo)
    assert str_to_mac(bar) == foo
    print inet_to_str('\x91\xfe\xa0\xed')
    assert inet_to_str('\x91\xfe\xa0\xed') == '145.254.160.237'
    assert str_to_inet('145.254.160.237') == '\x91\xfe\xa0\xed'
    assert is_internal('10.0.0.1')
    assert is_internal('222.2.2.2') == False
    assert is_special('224.0.0.251')
    assert is_special('224.0.0.252') == False

    my_iface = get_default_interface()
    print get_mac_address(my_iface)
    print 'Success!'

if __name__ == '__main__':
    test_utils()
