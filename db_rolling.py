
import pymongo
from pymongo import MongoClient
from config import MONGO_DB_ADDRESS
import time
import logging


IP = 'IP'
TCP = 'TCP'
ETHER = 'Ether'

# writeConcern = pymongo.write_concern.WriteConcern(w=0, wtimeout=None, j=None, fsync=None)
client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
scapy_database = client['scapy']
http_data_collection = scapy_database['tcpdatas']
tcpAggregatedDataString = 'tcpAggregatedData'
tcp_aggregated_data_collection = scapy_database[tcpAggregatedDataString]

  # .with_options(write_concern=writeConcern)


def one_day_before_milli_time():
  one_day_before = time.time() - 60 * 60 * 24
  return int(round(one_day_before * 1000))


def one_hour_before_milli_time():
  one_day_before = time.time() - 60 * 60
  return int(round(one_day_before * 1000))

def ten_minute_before_milli_time():
  ten_minute_before = time.time() - 60 * 10
  return int(round(ten_minute_before * 1000))


def twenty_minute_before_milli_time():
  ten_minute_before = time.time() - 60 * 20
  return int(round(ten_minute_before * 1000))

def main():
    logging.basicConfig(filename='db_rolling.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')
    try:
      time_to_be_deleted = ten_minute_before_milli_time()
      twenty_minute_before = twenty_minute_before_milli_time()
      # aggregate data
      results = http_data_collection.aggregate([
        {
          '$match': {
            'timestamp': {
              '$gt': twenty_minute_before,
              '$lt': time_to_be_deleted,
            },
          },
        },
        {
          '$group': {
            '_id': {
              'src_ip': '$src_ip',
              'dst_ip': '$dst_ip',
            },
            'totalPacketSize': { '$sum': '$packet_size' },
            'packetCount': { '$sum': 1 },
          },
        },
        {
          '$project': {
            '_id': 0,
            'totalPacketSize': 1,
            'packetCount': 1,
            'src_ip': '$_id.src_ip',
            'dst_ip': '$_id.dst_ip',
          },
        },
        {
          '$addFields': {
            'startMS': twenty_minute_before,
            'endMS': time_to_be_deleted,
          }
        },
        # {
        #   '$out': tcpAggregatedDataString,
        # },
      ])
      tcp_aggregated_data_collection.insert_many(results)
      # print(list(results))
      # delete data
      result = http_data_collection.delete_many({
        'timestamp': {
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

if __name__ == '__main__':
    main()