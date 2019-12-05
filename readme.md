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

