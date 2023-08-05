from calendar import c
from datetime import datetime, timedelta, date, time
from time import sleep
from dateutil.relativedelta import relativedelta
import psycopg2
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
from requests.exceptions import HTTPError
import csv
import sys
import os
import getopt
import verboselogs
import logging
import ssl
from itertools import zip_longest
import time
import sys

def fetch_dictionary(req, verify_location):
    resp =requests.get(req,verify=verify_location).json()

    return list(resp['states']) 

def fetch_snapshot(req, verify_location):
    resp =requests.get(req,verify=verify_location).json()
    radarID=resp['prefix'] #  To retrieve RadarID
    radarBand=radarID[5].capitalize()
    radar_letters = ''.join([part for part in radarID if not part.isdigit()])
    country = radar_letters.upper() 
    bb=list(resp['values'])

    return radarID,radarBand,bb,country
#dict_api.py
def write_to_influxdb(inputradarID, timeepo5min, radarBand, radarID, SubSyst_o, ShortName_o, StateValue, influx_url, influx_token, org, bucket,bb,country):
    points=[]
    for ii in range(len(bb)):
        measurement_name='LidarData' if inputradarID.startswith('lidar') else 'RadarData'
        val_other=[]
        try:
            points.append(influxdb_client.Point(measurement_name) \
                .tag("band", radarBand) \
                .tag("projectnumber", radarID) \
                .tag("subsystem", SubSyst_o[ii]) \
                .tag("country", country) \
                .field(ShortName_o[ii], float(StateValue[ii])) \
                .time(datetime.fromtimestamp(int(timeepo5min)), WritePrecision.NS) )
        except ValueError:
            points.append(influxdb_client.Point(measurement_name) \
                .tag("band", radarBand) \
                .tag("projectnumber", radarID) \
                .tag("subsystem", SubSyst_o[ii]+'str') \
                .tag("country", country) \
                .field(ShortName_o[ii], StateValue[ii]) \
                .time(datetime.fromtimestamp(int(timeepo5min)), WritePrecision.NS) )
                
                

    with InfluxDBClient(url=influx_url, token=influx_token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=points)
        client.close()
        print('check connect')




class DataCenter:
    def __init__(self,inputradarID,timeepo5min,url,token,ca_root_cert):
        print('hello')
        self.inputradarID= inputradarID
        print(self.inputradarID)
        self.timeepo5min=timeepo5min
        print(datetime.fromtimestamp(int(self.timeepo5min)))
        self.influx_url = url
        self.influx_token = token
        self.org = "Data"
        self.bucket = "Datacenter"
        self.context = ssl.SSLContext()
        self.context.load_verify_locations(ca_root_cert )
        self.req='https://localhost:8444/api/dictionary?prefix=' + self.inputradarID
        self.root_certificate=ca_root_cert
        #print('check')
        try:
            tt=fetch_dictionary(self.req, self.root_certificate)
            for group in zip_longest(*[iter(tt)]*200,fillvalue=None):
                aa=''
                SysState=[]
                SubSyst=[]
                ShortName=[]
                group = [x for x in group if x is not None]
                for x in group:
                    SysState.append(x['state'])
                    SubSyst.extend(x['subsystems'])
                    ShortName.append(x['shortname'])
                    aa=x['state']+','+aa

                reqe='https://localhost:8444/api/snapshot?prefix=' + self.inputradarID+ '&timestamp=' + self.timeepo5min + '000' + '&states=' + aa
                
                data_dict = dict(zip(SysState, zip(SubSyst, ShortName)))

                SubSyst_o=[]
                ShortName_o=[]
                SysState_o=[]
                StateValue=[]
                radarID,radarBand,bb,country=fetch_snapshot(reqe,self.root_certificate)
                for value in bb:
                    statename=value['statename']
                    if statename in data_dict:
                        SysState_o.append(statename)
                        SubSyst_o.append(data_dict[statename][0])
                        ShortName_o.append(data_dict[statename][1])
                        StateValue.append(value['value'])
                #print(np.unique(SubSyst_o))
                write_to_influxdb(self.inputradarID,self.timeepo5min,radarBand,radarID,SubSyst_o,ShortName_o,StateValue,self.influx_url,self.influx_token,self.org,self.bucket,bb,country)

        except Exception as err:
            print(f'Other error occurred: {err}')
if __name__=="__main__":
    #data_run=DataCenter('238aus20',str(int(time.time())))
    data_run=DataCenter(sys.argv[1],sys.argv[2])
