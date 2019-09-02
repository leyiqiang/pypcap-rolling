import pymongo
from pymongo import MongoClient
import time
from redis import StrictRedis, ConnectionPool
import json


class Database:
    def __init__(self, database_host, database_port):
        self.database_host = database_host
        self.database_port = database_port

    def add_packet_to_packet_set(self, packet):
        raise NotImplementedError("This method is not implemented in interface.")


class RedisDatabase:
    def __init__(self, database_host, database_port):
        # establish connections
        super().__init__(database_host, database_port)
        pool = ConnectionPool(host=database_host, port=database_port)
        self.redis = StrictRedis(connection_pool=pool)
        self.packet_dict = []
        self.time_tracker = {
            'last_time': time.time()
        }

    def add_packet_to_packet_set(self, packet):
        p_tuple = (packet['src_mac'], packet['dst_mac'])
        if p_tuple in self.packet_dict:
            self.packet_dict[p_tuple]['packetCount'] += 1
            self.packet_dict[p_tuple]['totalPacketSize'] += packet['packet_size']
            self.packet_dict[p_tuple]['endMS'] = packet['timestamp']
        else:
            obj = {
                'src_mac': packet['src_mac'],
                'dst_mac': packet['dst_mac'],
                'startMS': packet['timestamp'],
                'endMS': packet['timestamp'] + 100,
                'packetCount': 1,
                'totalPacketSize': packet['packet_size'],
            }
            self.packet_dict[p_tuple] = obj

        time_duration = 0.1  # 0.1s
        # if time duration > 0.1, insert the packet set into the database
        cur_time = time.time()
        # print(cur_time)
        if cur_time - self.time_tracker['last_time'] >= time_duration:
            self.time_tracker['last_time'] = cur_time
            # print(len(packet_list))
            # tcp_aggregated_data_collection.insert_many(packet_dict.values())
            for p in self.packet_dict.values():
                self.redis.zadd('packets', {json.dumps(p): p['startMS']})
            self.packet_dict.clear()


class MongodbDatabase(Database):
    def __init__(self, database_host, database_port):
        # establish connections
        super().__init__(database_host, database_port)
        writeConcern = pymongo.write_concern.WriteConcern(w=0, wtimeout=None, j=None, fsync=None)
        mongodb_address = database_host + ':' + database_port
        client = MongoClient(mongodb_address, serverSelectionTimeoutMS=1)
        scapy_database = client['scapy']
        self.http_data_collection = scapy_database['tcpdatas'].with_options(write_concern=writeConcern)

        self.packet_list = []
        self.time_tracker = {
            'last_time': time.time()
        }

    def add_packet_to_packet_set(self, packet):
        self.packet_list.append(packet)
        time_duration = 0.1  # 0.1s
        # if time duration > 0.1, insert the packet set into the database
        cur_time = time.time()
        # print(cur_time)
        if cur_time - self.time_tracker['last_time'] >= time_duration:
            self.time_tracker['last_time'] = cur_time
            # print(len(packet_list))
            self.http_data_collection.insert_many(self.packet_list)
            self.packet_list.clear()



