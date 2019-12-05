This project is modified based on https://github.com/VizIoT/pypcap-monitor

# pypcap-rolling
A python project to aggregate Redis Data into MongoDB database

## Crontab Configuration
```
* * * * * python3 /home/ubuntu/pypcap-monitor/start.py -c config.yml
```

## Python File Explanation:
1. [db_rolling.py](./db_rolling.py): Aggregate the data in a certain time based on configuration(default is 120 seconds)
2. [delete_aggregated_data.py](./delete_aggregated_data.py): delete the aggregated data from database
3. [databases.py](./databases.py): A file that contains the implementation of supported databases. Including get data from database, remove data from database and aggregate data
4. [start.py](./start.py): Start the project with configuration file.

## Config.yml File Explanation:
```
from_db_class_name: '<DB_CLASS_NAME>' # currently supports mongodb(MongodbDatabase) and redis(RedisDatabase)
to_db_class_name: '<DB_CLASS_NAME>' # currently supports mongodb(MongodbDatabase) and redis(RedisDatabase)
from_db_host: '<FROM_DB_HOST>'
from_db_port: '<FROM_DB_PORT>'
to_db_host: '<TO_DB_HOST>'
to_db_port: '<TO_DB_PORT>' # 27017 for mongodb, 6379 for redis
time_before: '<TIME_BEFORE>' # time before in seconds
```

