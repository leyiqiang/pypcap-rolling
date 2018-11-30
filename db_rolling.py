
import pymongo
from pymongo import MongoClient
from config import MONGO_DB_ADDRESS
import time


IP = 'IP'
TCP = 'TCP'
ETHER = 'Ether'

writeConcern = pymongo.write_concern.WriteConcern(w=0, wtimeout=None, j=None, fsync=None)
client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
scapy_database = client['scapy']
http_data_collection = scapy_database['tcpdatas'].with_options(write_concern=writeConcern)


def one_day_before_milli_time():
  one_day_before = time.time() - 60 * 60 * 24
  return int(round(one_day_before * 1000))

result = http_data_collection.delete_many({
  'timestamp': {
    '$lt': one_day_before_milli_time()
  }
})

