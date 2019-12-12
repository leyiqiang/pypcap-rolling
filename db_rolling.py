import databases
from itertools import groupby
from operator import itemgetter
import logging
import json
from util import get_timestamp_before_in_milliseconds, current_milli_time


class DBRolling(object):

  def __init__(self, from_db_class_name, to_db_class_name, from_db_host, to_db_host, from_db_port, to_db_port):
    self.from_db_class_name = from_db_class_name
    self.to_db_class_name = to_db_class_name
    self.from_db_host = from_db_host
    self.to_db_host = to_db_host
    self.from_db_port = from_db_port
    self.to_db_port = to_db_port
    FromDatabase = getattr(databases, self.from_db_class_name)
    self.from_db_instance = FromDatabase(self.from_db_host, self.from_db_port)
    ToDatabase = getattr(databases, self.to_db_class_name)
    self.to_db_instance = ToDatabase(self.to_db_host, self.to_db_port)

  def aggregate(self, time_before=2*60):
    data_before = [json.loads(b) for b in self.from_db_instance.get_data_before(time_before)]
    results = []
    grouper = itemgetter('src_mac', 'dst_mac')
    for key, grp in groupby(sorted(data_before, key=grouper), grouper):
      temp_dict = dict(zip(['src_mac', 'dst_mac'], key))
      total_packet_count = 0
      total_packet_size = 0
      for item in grp:
        total_packet_count += item['packetCount']
        total_packet_size += item['totalPacketSize']
      temp_dict['packetCount'] = total_packet_count
      temp_dict['totalPacketSize'] = total_packet_size
      temp_dict['timestamp'] = current_milli_time()
      results.append(temp_dict)
    try:
      self.to_db_instance.insert_aggregate_data(results)
    except Exception as e:
      logging.debug(e)
      return
    self.from_db_instance.delete_data_before(time_before)
    # db_instance = MyDatabase(self.database_host, self.database_port)
    # db_instance.aggregate_and_delete(time_before)

  def delete_aggregated_data(self, time_before=60*60*24):
    self.to_db_instance.aggregate_and_delete(time_before)
