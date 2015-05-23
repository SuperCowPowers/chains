#!/usr/bin/env python
"""
    Use DPKT to read in a pcap file and output the Ethernet Frames
"""
import dpkt
import datetime
import socket

# Local imports
from chains import stream_packets
from . import utils

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

def print_packets(packet_stream):
    """Print out information about each packet from a packet_stream

       Args:
           packet_stream: a packet_stream yields packets (timestamp, buf)
    """

    # For each packet in the pcap process the contents
    for timestamp, buf in packet_stream:

        # Print out the timestamp in UTC
        print 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp))

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)
        print 'Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type

        # Make sure the Ethernet frame contains an IP packet
        # EtherType (IP, ARP, PPPoE, IP6... see http://en.wikipedia.org/wiki/EtherType)
        if eth.type != dpkt.ethernet.ETH_TYPE_IP:  
            print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
            continue

        # Now unpack the data within the Ethernet frame (the IP packet) 
        # Pulling out src, dst, length, fragment info, TTL, and Protocol
        ip = eth.data

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        # Print out the info
        print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
              (ip_to_str(ip.src), ip_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset) 

def test():
    """Get a packet stream source and give it to print_packets :) """
    data_path = utils.relative_dir(__file__, '../data/http.pcap')
    packet_stream = stream_packets.stream_packets(iface_name = data_path, max_packets=10)
    print_packets(packet_stream)

if __name__ == '__main__':
    test()
