#!/usr/bin/python
import time
from scapy.all import *
from pymongo import MongoClient

from config import MONGO_DB_ADDRESS

client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
scapy_database = client['scapy']
http_data_collection = scapy_database['httpData']


def http_header(packet):
        # http_packet=str(packet)
        return GET_print(packet)
        # if http_packet.find('GET'):
        #         return GET_print(packet)


def GET_print(packet1):
    new_packet_obj = dict()
    # ret = "***************************************GET PACKET****************************************************\n"
    new_packet_obj['dstIP'] = packet1.sprintf("%IP.dst%")
    new_packet_obj['srcIP'] = packet1.sprintf("%IP.src%")
    new_packet_obj['dstMac'] = packet1.sprintf("%Ether.dst%")
    new_packet_obj['srcMac'] = packet1.sprintf("%Ether.src%")
    new_packet_obj['timestamp'] = time.time()
    http_data_collection.insert(new_packet_obj, w=0)
    print(new_packet_obj)
    # print('*****************************************************************************************************')
    # packet1.show()
    # ret += "*****************************************************************************************************\n"
    # return ret


sniff(iface='eth0', prn=http_header, filter="tcp port (80 or 443)")
# sniff(iface='eth0',
#       prn=http_header,
#       filter="(not ether host 06:11:5c:07:cc:2e) and tcp")
# sniff(iface='eth0',
#       prn=http_header,
#       filter="(not ip host 172.31.0.129) and tcp")


# def tcp_sniffing(pkt):
#     pkt.show()
#