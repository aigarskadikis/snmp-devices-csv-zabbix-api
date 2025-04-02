# Register SNMP devices from CSV via Zabbix API
The following project allows to onboard SNMP devices in Zabbix 7.2 from CSV.
It allows to automatically assign one host group and one template.
To not touch already registered objects, if "Host name" already exists, nothing will happen (no validation per host group and template)

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
