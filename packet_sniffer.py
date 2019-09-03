from scapy.all import *
from util import current_milli_time
from constants import IP, TCP, UDP, ETHER, FILTER, IFACE
import databases


class PacketSniffer(object):
    def __init__(self, db_class_name, database_host, database_port, sniff_config):
        self.db_class_name = db_class_name
        self.database_host = database_host
        self. database_port = database_port
        self.sniff_config = sniff_config
        # create database instance
        MyDatabase = getattr(databases, self.db_class_name)
        self.db_instance = MyDatabase(self.database_host, self.database_port)

    def http_header(self, packet):
        # http_packet=str(packet)
        return self.GET_print(packet)
        # if http_packet.find('GET'):
        #         return GET_print(packet)

    def GET_print(self, pkt):
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
            new_packet_obj['packet_size'] = len(pkt[TCP])
        if UDP in pkt:
            new_packet_obj['src_port'] = pkt[UDP].sport
            new_packet_obj['dst_port'] = pkt[UDP].dport
            new_packet_obj['packet_size'] = len(pkt[UDP])
        # new_packet_obj['dst_ip'] = packet1.sprintf("%IP.dst%")
        # new_packet_obj['src_ip'] = packet1.sprintf("%IP.src%")
        # new_packet_obj['dst_mac'] = packet1.sprintf("%Ether.dst%")
        # new_packet_obj['src_mac'] = packet1.sprintf("%Ether.src%")
        # new_packet_obj['src_port'] = packet1.sprintf("TCP.sport")
        # new_packet_obj['dst_port'] = packet1.sprintf("TCP.dport")
        new_packet_obj['timestamp'] = current_milli_time()
        # http_data_collection.insert_one(new_packet_obj)
        # add packet to the set
        self.db_instance.add_packet_to_packet_set(new_packet_obj)
        # print(len(pkt[TCP]))
        # print(new_packet_obj)
        # print('*****************************************************************************************************')
        # pkt.show()
        # ret += "*****************************************************************************************************\n"
        # return ret

    def start_sniffing(self):
        iface = self.sniff_config[IFACE]
        filter = self.sniff_config[FILTER]
        sniff(iface=iface, prn=self.http_header, filter=filter)
