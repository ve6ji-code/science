#!/usr/bin/python3
from urllib.request import urlopen
import warnings
import urllib.request
import json
import requests
import datetime
import pyMySql

# Get https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json

url = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json"


json_data = urlopen(url).read()
obj = json.loads(json_data)
obj.pop(0)
count = -300
obj = obj[count:]

#print(obj[count:])
for line in obj:
    date = line[0]
    date_prop = line[11]
    speed = line[1]    
    if speed is None:
        speed = 0
    density = line[2]
    if density is None:
        density = 0
    temperature = line[3]
    if temperature is None:
        temperature = 0
    bz = line[6]
    if bz is None:
        bz = 0
    bt = line[7]
    if bt is None:
        bt = 0
    #Solar Dynamic Pressure Formula 1.6726E-6 * density * speed^2
    speed = float(speed)
    density = float(density)
    dyn_press = (1.6726E-6 * density * pow(speed,2))
    time_tag = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    time_tag_prop = datetime.datetime.strptime(
        date_prop, "%Y-%m-%d %H:%M:%S.%f")
    unix_epoch = int(time_tag.timestamp())
    unix_epoch_prop = int(time_tag_prop.timestamp())
    delta_time = int((unix_epoch_prop - unix_epoch)/60)
    # print(line)
    # Sbreak
    # Create INSERT statement per line
    stmnt = ("INSERT HIGH_PRIORITY INTO NOAA_SWPC_Solar_Prop VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(
        unix_epoch, time_tag, unix_epoch_prop, time_tag_prop, delta_time, speed, temperature, density, bz, bt, dyn_press))
    #print(stmnt)
    # from pyMySql.py
    pyMySql.Insert(stmnt)
