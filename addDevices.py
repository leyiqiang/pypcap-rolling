import databases


def add_device(db_class_name, database_host, database_port):
  MyDatabase = getattr(databases, db_class_name)
  db_instance = MyDatabase(database_host, database_port)
  db_instance.add_device()
