
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
http_data_collection = scapy_database['tcpdatas']\
  # .with_options(write_concern=writeConcern)


def one_day_before_milli_time():
  one_day_before = time.time() - 60 * 60 * 24
  return int(round(one_day_before * 1000))


def main():
    logging.basicConfig(filename='db_rolling.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')
    try:
      time_to_be_deleted = one_day_before_milli_time()
      result = http_data_collection.delete_many({
        'timestamp': {
          '$lt': time_to_be_deleted
        }
      })
      logging.info('delete entries before ' + str(time_to_be_deleted))
      logging.info('number of records deleted: ' + str(result.deleted_count))
    except Exception as e:
      logging.error('Error: ' + str(e))
    logging.info('Finished')

if __name__ == '__main__':
    main()