# snmp-devices-csv-zabbix-api
Following project allows to onboard SNMPv2 devices in Zabbix 7.2 from CSV and automatically assign one host group and one template.

Input file must consist with 2 columns:
```csv
Host name,IP address
abrakadabra,192.168.88.1
helloWorld,10.10.10.10
NewHost2,10.15.16.17
Zabbix server,88.88.88.88
```

On Linux set script executable:
```bash
chmod +x onboard.py
```

Run on Linux:
```bash
./onboard.py \
--api_jsonrpc https://127.0.0.1:44372/api_jsonrpc.php \
--token c40909c684312e2d8c2ca59811cc034e90ac31448a9e9ede8d70f3564aedcdf3 \
--csv devices.csv \
--defaultTemplate='Generic by SNMP' \
--defaultHostGroup 'Discovered hosts'
```

Run on Windows:
```
python3 onboard.py \
--api_jsonrpc https://127.0.0.1:44372/api_jsonrpc.php \
--token c40909c684312e2d8c2ca59811cc034e90ac31448a9e9ede8d70f3564aedcdf3 \
--csv devices.csv \
--defaultTemplate='Generic by SNMP' \
--defaultHostGroup 'Discovered hosts'
```
