import databases


class DBRolling(object):

  def __init__(self, db_class_name, database_host, database_port):
    self.db_class_name = db_class_name
    self.database_host = database_host
    self.database_port = database_port
    MyDatabase = getattr(databases, self.db_class_name)
    self.db_instance = MyDatabase(self.database_host, self.database_port)

  def aggregate(self, time_before=2*60):
    MyDatabase = getattr(databases, self.db_class_name)
    db_instance = MyDatabase(self.database_host, self.database_port)
    db_instance.aggregate_and_delete(time_before)

  def delete_aggregated_data(self, time_before=60*60*24):
    self.db_instance.delete_aggreated_data(time_before)
