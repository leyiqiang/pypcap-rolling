import databases
# import pymongo
# from pymongo import MongoClient
# from config import MONGO_DB_ADDRESS
# import time
# import logging

# client = MongoClient(MONGO_DB_ADDRESS, serverSelectionTimeoutMS=1)
# scapy_database = client['scapy']
# device_collection = scapy_database['devices']
  # .with_options(write_concern=writeConcern)


def add_device(db_class_name, database_host, database_port):
  MyDatabase = getattr(databases, db_class_name)
  db_instance = MyDatabase(database_host, database_port)
  db_instance.add_device()
  # fname = 'devices.txt'
  # deviceList = []
  # with open(fname) as f:
  #   for line in f:
  #     macAddress, name = line.strip().split(' ')
  #     deviceList.append({
  #       'macAddress': macAddress,
  #       'name': name,
  #     })
  # device_collection.insert_many(deviceList)


# if __name__ == '__main__':
#     main()
