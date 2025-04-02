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
    parser.add_argument('--csv',help="'devices.csv'",type=str,required=True)
    parser.add_argument('--defaultTemplate',help="'Generic by SNMP'",type=str,required=True)
    parser.add_argument('--defaultHostGroup',help="'Discovered hosts'",type=str,required=True)

    args = parser.parse_args()

    url = args.api_jsonrpc
    token = args.token
    inputFile = args.csv
    defaultTemplate = args.defaultTemplate
    defaultHostGroup = args.defaultHostGroup

    # define token in header
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}

    
    # existing host objects
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {"output": ["hostid","host"]},
        "id": 1
    })
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        raw_text = response.text
        #print("Raw JSON response:", raw_text)
        json_response = json.loads(raw_text)
        existingHostList = parse('$.result').find(json_response)[0].value
    except Exception as e:
        print("Error occurred:", str(e))


    # existing template objects
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {"output": ["templateid","host"]},
        "id": 1
    })
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        raw_text = response.text
        #print("Raw JSON response:", raw_text)
        json_response = json.loads(raw_text)
        existingTemplateList = parse('$.result').find(json_response)[0].value
    except Exception as e:
        print("Error occurred:", str(e))


    # existing host group objects
    payload = json.dumps({"jsonrpc":"2.0","method":"hostgroup.get","params":{"output":["groupid","name"]},"id":1})
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        raw_text = response.text
        #print("Raw JSON response:", raw_text)
        json_response = json.loads(raw_text)
        existingHostGroupList = parse('$.result').find(json_response)[0].value
    except Exception as e:
        print("Error occurred:", str(e))


    # locate ID for default template object
    templateid = 0
    for template in existingTemplateList:
        if template["host"] == defaultTemplate:
            templateid = template["templateid"]
            break


    # locate ID for default host group
    hostgroupid = 0
    for hg in existingHostGroupList:
        if hg["name"] == defaultHostGroup:
            hostgroupid = hg["groupid"]
            break


    # pick up CSV file
    with open(inputFile, 'rt') as f:
        # Convert to a list for immediate use
        deviceList = list(csv.DictReader(f))

    print("")
    # go through CSV
    for device in deviceList:
        # print name
        print("checking: "+ device['Host name'])
        # host group not recognized yet
        hostExist = 0
        # go through existing
        for existing in existingHostList:
            if device['Host name'] == existing['host']:
                # mask host group as found
                hostExist = 1
                print('already exists')
                break

        # if host is not yet registered
        if not hostExist:

            print('not exist. will try to create')

            # if defaul template exists
            if int(templateid) > 0:

                # if host group exists
                if int(hostgroupid) > 0:

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
                                    "ip": device['IP address'],
                                    "dns": "",
                                    "port": "161",
                                    "details":{"version":"2","bulk": "1","community":"not.important.for.SNMP.traps"}
                                }
                            ],
                            "groups": [{"groupid": hostgroupid}],
                            "templates": [{"templateid": templateid}]
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
                else:
                    print("cannot create because host group '"+ defaultHostGroup + "' does not exist")
            else:
                print("cannot create because template: '"+ defaultTemplate + "' does not exist")

        print("")


if __name__ == "__main__":
    main()

