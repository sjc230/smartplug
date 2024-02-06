'''
Author: Qi7
Date: 2023-01-18 09:43:57
LastEditors: aaronli-uga ql61608@uga.edu
LastEditTime: 2023-01-18 09:44:46
Description: 
'''
import time
import math
import subprocess
import sys
import random
import webbrowser
import numpy as np
from datetime import datetime
from dateutil import tz
import pytz
from influxdb import InfluxDBClient
import operator
# python API client for influx 2.x
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def write_influx2(influx, unit, table_name, data_name, data, start_timestamp, fs):
    """This function shows an example how to write a point into the influx 2.x database
    Args:
        influx (_type_): _description_
        unit (_type_): _description_
        table_name (_type_): _description_
        data_name (_type_): _description_
        data (_type_): _description_
        start_timestamp (_type_): _description_
        fs (_type_): _description_
    """
    
    bucket = "<my-bucket>"
    org = "<my-org>"
    token = "<my-token>"
    # Store the URL of your InfluxDB instance
    url="http://localhost:8086"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
    write_api.write(bucket=bucket, org=org, record=p)
    return

def read_influx2(influx, unit, table_name, data_name, start_timestamp, end_timestamp, condition="location"):
    """This function shows an example how to read data points from influx 2.x database
    Args:
        influx (_type_): _description_
        unit (_type_): _description_
        table_name (_type_): _description_
        data_name (_type_): _description_
        start_timestamp (_type_): _description_
        end_timestamp (_type_): _description_
        condition (str, optional): _description_. Defaults to "location".
    """
    bucket = "<my-bucket>"
    org = "<my-org>"
    token = "<my-token>"
    # Store the URL of your InfluxDB instance
    url="http://localhost:8086"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    
    query_api = client.query_api()
    query = ‘ from(bucket:"my-bucket")\
    |> range(start: -10m)\
    |> filter(fn:(r) => r._measurement == "my_measurement")\
    |> filter(fn: (r) => r.location == "Prague")\
    |> filter(fn:(r) => r._field == "temperature" )‘
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    print(results)
    return