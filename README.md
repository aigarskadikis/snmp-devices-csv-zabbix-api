# snmp-devices-csv-zabbix-api
Onboard SNMPv2 devices in Zabbix 7.2 from CSV


create input file in format
```csv
Host name,IP address
abrakadabra,192.168.88.1
helloWorld,10.10.10.10
NewHost2,10.15.16.17
Zabbix server,88.88.88.88
```

usage
```bash
./onboard.py \
--api_jsonrpc https://127.0.0.1:44372/api_jsonrpc.php \
--token c40909c684312e2d8c2ca59811cc034e90ac31448a9e9ede8d70f3564aedcdf3 \
--csv devices.csv \
--defaultTemplate='Generic by SNMP' \
--defaultHostGroup 'Discovered hosts'
```

or on windows
```
python3 onboard.py \
--api_jsonrpc https://127.0.0.1:44372/api_jsonrpc.php \
--token c40909c684312e2d8c2ca59811cc034e90ac31448a9e9ede8d70f3564aedcdf3 \
--csv devices.csv \
--defaultTemplate='Generic by SNMP' \
--defaultHostGroup 'Discovered hosts'
```
