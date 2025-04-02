#!/usr/bin/env python3.9
import argparse
import yaml

import csv
import json
from jsonpath_ng import parse
import requests
import urllib3


def main():

    urllib3.disable_warnings()


    parser = argparse.ArgumentParser()
    parser.add_argument('--api_jsonrpc',help="'https://127.0.0.1:44372/api_jsonrpc.php'",type=str,required=True)
    parser.add_argument('--token',help="'c40909c684312e2d8c2ca59811cc034e90ac31448a9e9ede8d70f3564aedcdf3'",type=str,required=True)

    # LDAP settings
    parser.add_argument('--csv',help="'devices.csv'",type=str,required=True)

    args = parser.parse_args()

    url = args.api_jsonrpc
    token = args.token
    inputFile = args.csv


    # pick up all host titles, load into memory
    # read csv
    # per every line:
    #   look if hostname already exists
    #   if exist:
    #     do nothing
    #   else:
    #     host.create, link template


    # define token in header
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}

    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
                "hostid",
                "host"
            ]
        },
        "id": 1
    })

    # observe existing host objects
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        raw_text = response.text
        print("Raw JSON response:", raw_text)
        json_response = json.loads(raw_text)
        existingHostList = parse('$.result').find(json_response)[0].value
    except Exception as e:
        print("Error occurred:", str(e))

    # pick up CSV file
    with open(inputFile, 'rt') as f:
        # Convert to a list for immediate use
        deviceList = list(csv.DictReader(f))

    # go through CSV
    for device in deviceList:
        # print name
        print(device['Host name'])
        # host group not recognized yet
        hostExist = 0
        # go through existing
        for existing in existingHostList:
            if device['Host name'] == existing['host']:
                # mask host group as found
                hostExist = 1
                print(device['Host name'] + ' exists')
                break

        if not hostExist:

            payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "host.create",
                "params": {
                    "host": device['Host name'],
                    "interfaces": [
                        {
                            "type": 2,
                            "main": 1,
                            "useip": 1,
                            "ip": "127.0.0.1",
                            "dns": "",
                            "port": "161",
                            "details": {
                                "version": "2",
                                "bulk": "1",
                                "community": "not.important.for.SNMP.traps"
                            }
                        }
                    ],
                    "groups": [
                        {
                            "groupid": "5"
                        }
                    ],
                    "templates": [
                        {
                            "templateid": "10563"
                        }
                    ]
                },
                "id": 1
            })

            try:
                response = requests.request("POST", url, headers=headers, data=payload, verify=False)

                raw_text = response.text
                print("Raw JSON response:", raw_text)
                json_response = json.loads(raw_text)
                #existingHostList = parse('$.result').find(json_response)[0].value
            except Exception as e:
                print("Error occurred:", str(e))


if __name__ == "__main__":
    main()

