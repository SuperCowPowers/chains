"""Network utilities that might be useful"""
import socket
import json

# Local imports
from chains.utils import file_utils

def mac_to_str(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address: a MAC address
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02X' % ord(b) for b in address)

def mac_to_host(address):
    """Lookup host with a MAC address (requires a hosts.json file)

       Args:
           address: a MAC address
       Returns:
           str: Hostname if found else None
    """
    # Try to load the host_map
    if not hasattr(mac_to_host, 'host_map'):
        data_path = file_utils.relative_dir(__file__, '../../data/hosts.json')
        try:
            with open(data_path) as host_fp:
                mac_to_host.host_map = json.load(host_fp)
        except IOError:
            mac_to_host.host_map = {}

    # Return the host associated with this MAC address
    return mac_to_host.host_map.get(address)

def ip_to_str(inet):
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
    print mac_to_host('\x01\x02\x03\x04\x05\x06')
    assert mac_to_host('\x01\x02\x03\x04\x05\x06') == None
    print ip_to_str('\x91\xfe\xa0\xed')
    assert ip_to_str('\x91\xfe\xa0\xed') == '145.254.160.237'
    assert is_internal('10.0.0.1')
    assert is_internal('222.2.2.2') == False
    assert is_special('224.0.0.251')
    assert is_special('224.0.0.252') == False
    print 'Success!'

if __name__ == '__main__':
    test_utils()
