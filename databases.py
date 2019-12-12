from pymongo import MongoClient
import time
from redis import StrictRedis, ConnectionPool
import json
import logging
from util import get_timestamp_before_in_milliseconds, current_milli_time


class Database:
    def __init__(self, database_host, database_port):
        self.database_host = database_host
        self.database_port = database_port


class RedisDatabase(Database):
    def __init__(self, database_host, database_port):
        # establish connections
        super().__init__(database_host, database_port)
        pool = ConnectionPool(host=database_host, port=database_port)
        self.redis = StrictRedis(connection_pool=pool)
        self.packet_dict = {}
        self.time_tracker = {
            'last_time': time.time()
        }

    def get_data_before(self, time_before):
        cur_time_in_ms = current_milli_time()
        data = self.redis.zrangebyscore('packets', cur_time_in_ms - time_before * 1000, cur_time_in_ms)
        return data

    def get_and_delete_data_before(self, time_before):
        cur_time_in_ms = current_milli_time()
        data = self.redis.zrangebyscore('packets', cur_time_in_ms - time_before * 1000, cur_time_in_ms)
        self.redis.zremrangebyscore('packets', cur_time_in_ms - time_before * 1000, cur_time_in_ms)
        return data

    def delete_data_before(self, time_before):
        cur_time_in_ms = current_milli_time()
        self.redis.zremrangebyscore('packets', cur_time_in_ms - time_before * 1000, cur_time_in_ms)


class MongodbDatabase(Database):
    def __init__(self, database_host, database_port):
        # establish connections
        super().__init__(database_host, database_port)
        # writeConcern = pymongo.write_concern.WriteConcern(w=0, wtimeout=None, j=None, fsync=None)
        mongodb_address = database_host + ':' + database_port
        client = MongoClient(mongodb_address, serverSelectionTimeoutMS=1)
        scapy_database = client['scapy']
        self.http_data_collection = scapy_database['tcpdatas']#.with_options(write_concern=writeConcern)
        self.device_collection = scapy_database['devices']
        tcpAggregatedDataString = 'tcpAggregatedData'
        self.tcp_aggregated_data_collection = scapy_database[tcpAggregatedDataString]
        self.packet_list = []
        self.time_tracker = {
            'last_time': time.time()
        }


    def add_device(self):
        fname = 'devices.txt'
        deviceList = []
        with open(fname) as f:
            for line in f:
                macAddress, name = line.strip().split(' ')
                deviceList.append({
                    'macAddress': macAddress,
                    'name': name,
                })
        self.device_collection.insert_many(deviceList)

    def insert_aggregate_data(self, results):
        self.http_data_collection.insert_many(results)

    # aggregate the data before certain time, delete the original data after aggregation
    def aggregate_and_delete(self, time_before):
        logging.basicConfig(filename='db_rolling.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info('Started')
        try:
            time_to_be_deleted = get_timestamp_before_in_milliseconds(1 * 60)  # 1 mins
            start_time = get_timestamp_before_in_milliseconds(time_before)

            # aggregate data
            results = self.http_data_collection.aggregate([
                {
                    '$match': {
                        'timestamp': {
                            '$gt': start_time,
                            '$lt': time_to_be_deleted,
                        },
                    },
                },
                {
                    '$group': {
                        '_id': {
                            'src_mac': '$src_mac',
                            'dst_mac': '$dst_mac',
                        },
                        'totalPacketSize': {'$sum': '$packet_size'},
                        'packetCount': {'$sum': 1},
                    },
                },
                {
                    '$project': {
                        '_id': 0,
                        'totalPacketSize': 1,
                        'packetCount': 1,
                        'src_mac': '$_id.src_mac',
                        'dst_mac': '$_id.dst_mac',
                    },
                },
                {
                    '$addFields': {
                        'startMS': start_time,
                        'endMS': time_to_be_deleted,
                    }
                },
                # {
                #   '$out': 'tcpAggregatedData',
                # },
            ])
            print(list(results))
            self.tcp_aggregated_data_collection.insert_many(results)
            # delete data
            result = self.http_data_collection.delete_many({
                'timestamp': {
                    '$lt': time_to_be_deleted
                }
            })
            deleted_count = result.deleted_count

            logging.info('delete entries before ' + str(time_to_be_deleted))
            logging.info('number of records deleted: ' + str(deleted_count))
        except Exception as e:
            raise(e)
            print('Error: ' + str(e))
            logging.error('Error: ' + str(e))
        logging.info('Finished')

    def delete_aggreated_data(self, time_before):
        logging.basicConfig(filename='db_rolling2.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info('Started')
        try:
            time_to_be_deleted = get_timestamp_before_in_milliseconds(time_before)

            # print(list(results))
            # delete data
            result = self.tcp_aggregated_data_collection.delete_many({
                'endMS': {
                    '$lt': time_to_be_deleted
                }
            })
            deleted_count = result.deleted_count

            logging.info('delete entries before ' + str(time_to_be_deleted))
            logging.info('number of records deleted: ' + str(deleted_count))
        except Exception as e:
            print(e)
            logging.error('Error: ' + str(e))
        logging.info('Finished')



