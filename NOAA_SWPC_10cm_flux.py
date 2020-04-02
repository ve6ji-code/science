#!/usr/bin/python3
import warnings
import urllib.request, json, requests
import datetime
import pyMySql

# Get https://services.swpc.noaa.gov/products/10cm-flux-30-day.json

url = "https://services.swpc.noaa.gov/products/10cm-flux-30-day.json"

from urllib.request import urlopen

json_data = urlopen(url).read()
obj = json.loads(json_data)
obj.pop(0)
for line in obj:
    date = line[0]
    flux = line[1]
    time_tag = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
    unix_epoch = int(time_tag.timestamp())
    # Create INSERT statement per line
    stmnt = ("INSERT HIGH_PRIORITY INTO NOAA_SWPC_10cm_Flux VALUES('{0}','{1}','{2}')".format(unix_epoch,time_tag,flux))
    print(stmnt)
    # from pyMySql.py
    pyMySql.Insert(stmnt)
