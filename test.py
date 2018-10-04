#!/usr/bin/python
from scapy.all import *


def http_header(packet):
        http_packet=str(packet)
        if http_packet.find('GET'):
                return GET_print(packet)


def GET_print(packet1):
    ret = "***************************************GET PACKET****************************************************\n"
    ret += packet1.sprintf("Destination:%IP.dst%")
    packet1.show()
    ret += "*****************************************************************************************************\n"
    return ret


sniff(iface='eth0', prn=http_header, filter="tcp port 80")