
# pypcap-monitor
A python project to sniff the internet traffic and stored it into 
MongoDB database. 
## How To Run
```bash
tmux attach
./make.sh-run.sh &
./kill &
tmux detach
```
1. Use [tmux](https://github.com/tmux/tmux) to create a session
2. Run make-run.sh script to keep the python script running
3. Run kill.sh script to kill the python script every 30 minutes.

## Python File Explanation:
1. [sniff.py](./sniff.py): Use [scapy](https://github.com/secdev/scapy) library to
sniff the data. Insert the sniffed data into a MongoDB.
2. [db_rolling.py](./db_rolling.py): Aggregate the data in the last two minutes
3. [db_rolling2.py](./db_rolling2.py): delete the aggregated data 1 week before
4. config.py: the MongoDB Address. This file should not be pushed
to GitHub. Use [config-example.py](./config-example.py) as an example.
MONGO_DB_ADDRESS = '<MONGO_DB_ADDRESS>'.
5. [addDevices.py](./addDevices.py): Read the device mac and name information from
a file in the router. Store the device information into the MongoDB

## Crontab Configuration
```
*/2 * * * * python3 [path]/pypcap-monitor/db_rolling.py # every 2 minutes
0 * * * * python3 [path]/pypcap-monitor/db_rolling2.py # every hour 
```

## Scapy Configuration
Ask Daniel for which iface should be listened to in the router
```python
  # sniff iface en0 of all tcp and udp packets
  sniff(iface='en0', prn=http_header, filter="tcp or udp")
  
  # sniff iface en0 of tcp port 80 and 443 packets
  sniff(iface='en0', prn=http_header, filter="tcp port (80 or 443)")
  
  # sniff iface en1 of tcp port 80 and 443 packets
  sniff(iface='eth1', prn=http_header, filter="tcp port (80 or 443)", store=0)
  
  # sniff iface eth1 of all tcp and udp packets
  sniff(iface='eth1', prn=http_header, filter="tcp or udp")
```