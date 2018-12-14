#!/usr/bin/python3
import time
from scapy.all import *
import pymongo
from pymongo import MongoClient
from config import MONGO_DB_ADDRESS



IP = 'IP'
TCP = 'TCP'
UDP = 'UDP'
ETHER = 'Ether'

writeConcern = pymongo.write_concern.WriteConcern(w=0, wtimeout=None, j=None, fsync=None)
client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
scapy_database = client['scapy']
http_data_collection = scapy_database['tcpdatas'].with_options(write_concern=writeConcern)


def http_header(packet):
  # http_packet=str(packet)
  return GET_print(packet)
  # if http_packet.find('GET'):
  #         return GET_print(packet)


def current_milli_time():
  return int(round(time.time() * 1000))


def GET_print(pkt):
  new_packet_obj = dict()
  # ret = "***************************************GET PACKET****************************************************\n"
  if ETHER in pkt:
    new_packet_obj['dst_mac'] = pkt[ETHER].dst
    new_packet_obj['src_mac'] = pkt[ETHER].src
  if IP in pkt:
    new_packet_obj['src_ip'] = pkt[IP].src
    new_packet_obj['dst_ip'] = pkt[IP].dst
  if TCP in pkt:
    new_packet_obj['src_port'] = pkt[TCP].sport
    new_packet_obj['dst_port'] = pkt[TCP].dport
    new_packet_obj['size'] = len(pkt[TCP])
  if UDP in pkt:
    new_packet_obj['src_port'] = pkt[UDP].sport
    new_packet_obj['dst_port'] = pkt[UDP].dport
    new_packet_obj['size'] = len(pkt[UDP])
  # new_packet_obj['dst_ip'] = packet1.sprintf("%IP.dst%")
  # new_packet_obj['src_ip'] = packet1.sprintf("%IP.src%")
  # new_packet_obj['dst_mac'] = packet1.sprintf("%Ether.dst%")
  # new_packet_obj['src_mac'] = packet1.sprintf("%Ether.src%")
  # new_packet_obj['src_port'] = packet1.sprintf("TCP.sport")
  # new_packet_obj['dst_port'] = packet1.sprintf("TCP.dport")
  new_packet_obj['timestamp'] = current_milli_time()

  http_data_collection.insert_one(new_packet_obj)
  # print(len(pkt[TCP]))
  # print(new_packet_obj)
  # print('*****************************************************************************************************')
  # pkt.show()
  # ret += "*****************************************************************************************************\n"
  # return ret

if __name__ == '__main__':

  # sniff(iface='en0', prn=http_header, filter="tcp or udp")
  # sniff(iface='en0', prn=http_header, filter="tcp port (80 or 443)")
  sniff(iface='eth1', prn=http_header, filter="tcp port (80 or 443)")
