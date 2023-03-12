import os
import time
import socket
import struct
import ctypes
import threading

from netaddr import IPNetwork, IPAddress
from ICMPHeader import ICMP


# host to listen on
HOST = '192.168.1.114'

# subnet to target (iterates through all IP address in this subnet)
SUBNET = '192.168.1.0/24'

# string signature
MESSAGE = 'hellooooo'



def udp_sender(SUBNET, MESSAGE):
    ''' Sprays out the udp datagram'''
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in IPNetwork(SUBNET):
        try:
            sender.sendto(MESSAGE, (str(ip), 65212))
        except:
            pass



def main():

    t = threading.Thread(target=udp_sender, args=(SUBNET, MESSAGE))
    t.start()
    socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind(( HOST, 0 ))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # continually read in packets and parse their information
    while True:
        raw_buffer = sniffer.recvfrom(65565)[0]
        ip_header = raw_buffer[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s' , ip_header)

        # Create our IP structure
        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        src_addr = socket.inet_ntoa(iph[8]);

        # Create our ICMP structure
        buf = raw_buffer[iph_length:iph_length + ctypes.sizeof(ICMP)]
        icmp_header = ICMP(buf)
        
        # check for the type 3 and code and within our target subnet
        if icmp_header.code == 3 and icmp_header.type == 3:
            if IPAddress(src_addr) in IPNetwork(SUBNET):
                if raw_buffer[len(raw_buffer) - len(MESSAGE):] == MESSAGE:
                    print(f'Host up: {src_addr}')


if __name__ == '__main__':
    main()