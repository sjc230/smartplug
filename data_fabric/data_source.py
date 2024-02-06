'''
Author: Qi7
Date: 2023-01-23 13:21:38
LastEditors: aaronli-uga ql61608@uga.edu
LastEditTime: 2023-02-07 21:04:11
Description: Generating Synthetic sine waveform and write to influxdb 2.6
'''
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime, time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

#
token = "sSDR3urw9jxgsqq4q45MkUHZ4pqloQuKt_8MNTPoz8mEu4Nx4TRKXApZBTR-4QIz0XHcWrykWWm__9eoW9QLQQ=="
bucket = "theBucket"
org = "sevenSun"
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
# write script
write_api = client.write_api(write_options=SYNCHRONOUS)

timestamp = datetime.datetime.now().timestamp()
F = 1 # frequency of the sine waveform
Fs = 50 # sampling frequency
Ts = 1./Fs
Mag = 1 # magnitude 
status = "normal"
if status == "abnormal":
    # add gaussion noise to the signal
    noise = np.random.normal(0, 1*0.3)
else:
    noise = 0

while True:
    for _ in range(Fs):
        timestamp += 1 / Fs
        value = Mag * math.sin(2 * math.pi * F * timestamp) + noise
        p = influxdb_client.Point("waveform").tag("status", status).field("current", value)
        write_api.write(bucket=bucket, org=org, record=p)
        time.sleep(Ts)