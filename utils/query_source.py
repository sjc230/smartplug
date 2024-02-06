'''
Author: Qi7
Date: 2023-01-23 16:15:49
LastEditors: aaronli-uga ql61608@uga.edu
LastEditTime: 2023-02-28 20:40:40
Description: query the data from influxDB
'''
import numpy as np
import math
import matplotlib.pyplot as plt
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import sys
sys.path.append('../')
from utils.sliding_window import sliding_windows # import helper function from AI engine module

token = "sSDR3urw9jxgsqq4q45MkUHZ4pqloQuKt_8MNTPoz8mEu4Nx4TRKXApZBTR-4QIz0XHcWrykWWm__9eoW9QLQQ=="
bucket = "theBucket"
org = "sevenSun"
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Query script
start = "2023-01-25T03:39:32Z"
stop = "2023-01-25T03:40:03Z"
measurement = "temp"
field = "current"
host = ""

status = "abnormal" # to prompt the data's label
if status == "normal":
    label = 0
else:
    label = 1

query_api = client.query_api()
query = f'from(bucket:"{bucket}")\
|> range(start: {start}, stop: {stop})\
|> filter(fn:(r) => r._measurement == "{measurement}")\
|> filter(fn:(r) => r.status == "{status}")\
|> filter(fn:(r) => r._field == "{field}")'

result = query_api.query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        # results.append((record.get_field(), record.get_value()))
        results.append(record.get_value())
        


x = sliding_windows(results, 20, 2)

# Adding the label information to the matrix
Y = [label] * x.shape[0]
Y = np.array(Y)
Y = Y.reshape((-1,1))
npy_data = np.concatenate((x, Y), axis = 1)

# print(npy_data)
# with open('abnormal.npy', 'wb') as f:
#     np.save(f, npy_data)