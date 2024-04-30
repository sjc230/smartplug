import paho.mqtt.client as mqtt
import subprocess
from datetime import datetime, timedelta

import yaml
import time
import numpy as np
    

def array_to_string(data):
    returnDataString = ""
    for i in range(len(data) - 2):
        returnDataString += str(data[i]) + ","
    
    returnDataString += str(data[len(data)-1])
    return returnDataString

# Turn the data String into a list
def string_to_list(dataString):
    data = dataString.split(",")
    return data
    
# # New influx
def write_influx_test(influx, influx_ip, influx_user, influx_pass, data):
    
    # put into config file soon
    # influxConfig = {}
    # influxConfig["influx_ip"] = 'https://sensorweb.us'
    # influxConfig["influx_user"] = 'test'
    # influxConfig["influx_pass"] =  'sensorweb'
    
    start_timestamp = influx['start_timestamp'] / 1000000
    
    ## function to parse data
    http_post  = "curl -i -k -XPOST \'"+ "https://" + influx_ip +":8086/write?db="+influx['db_name']+"\' -u "+ influx_user +":"+ influx_pass +" --data-binary \' "
    count = 0
    dataLength = len(data)
    for value in data:
        count += 1
        http_post += "\n" + influx['table_name'] +",location=" + influx['mac_address'] + " "
        http_post += influx['data_name'] + "=" + str(value) + " " + str(int(start_timestamp*10e8))
        start_timestamp +=  influx['interval'] / 1000000
            
    http_post += "\'  &"
    print(http_post)
    subprocess.call(http_post, shell=True)
    print("printed to iflux!")



def get_epoch_time():
    return round(time.time(), 3)

def create_sine_wave(influx_packet,influx_frequency):
    
    maxTime = influx_packet * influx_frequency
    DataValues = 10 * np.sin(2 * np.pi * np.linspace(0, maxTime, influx_packet) / 1)
    DataValues = np.round(DataValues, decimals = 2)
    
    return DataValues
# ===================================================================================
# This function parses the config file and returns a list of values
def get_config_info():
    config_dict = {}
    with open("config.yaml", "r") as stream:
        config_dict = yaml.safe_load(stream)

    return config_dict

#==================================================

# This function write an array of data to influxdb. 
# influx - the InfluxDB info including ip, db, user, pass. Example influx = {'ip': 'https://sensorweb.us', 'db': 'algtest', 'user':'test', 'passw':'sensorweb'}
# dataname - the dataname such as temperature, heartrate, etc
# timestamp - the epoch time (in second) of the first element in the data array, such as datetime.now().timestamp()
# unit - the unit location name tag, in general use MAC address to identify an unit

def write_influx(influx, data):

    influx_timestamp=int(influx['start_timestamp'] / 10000) # micro second change to 10 millisecond
    
    max_size = 120
    count = 0
    total = len(data)
    prefix_post  = "curl -k -POST \'" + "https://" +  influx['ip']+":8086/write?db="+influx['db_name']+"\' -u "+ influx['user']+":"+ influx['passw']+" --data-binary \' "
    http_post = prefix_post
    for value in data:
        count += 1
        http_post += "\n" + influx['table_name'] +",location=" + influx['mac_address'] + " "
        influx_time_string=str(influx_timestamp) #'{:d}'.format(influx_timestamp)
        http_post += influx['data_name'] + "=" + str(value) + " " + influx_time_string + "0000000"

        #print("write influx start_timestamp",http_post)

        influx_timestamp +=int(influx['interval'] / 10000)

        if(count >= max_size):
            http_post += "\'  &"
            # if debug: print(http_post)
            # print("Write to influx: ", table_name, data_name, count)
            subprocess.call(http_post, shell=True)
            total = total - count
            count = 0
            http_post = prefix_post
    if count != 0:
        http_post += "\'  &"
        # print(http_post)
        # print("Write to influx: ", table_name, data_name, count, data)
        subprocess.call(http_post, shell=True)

# def timestamp_to_timeofday(timestamp):
#     microseconds_since_epoch = timestamp
#     seconds_since_epoch = microseconds_since_epoch // 1_000_000

#     # 使用 timedelta 和 datetime 将秒数转换为具体的日期和时间
#     timeofday = datetime(1970, 1, 1) + timedelta(seconds=seconds_since_epoch)
#     # 将时间转换为东八区时间
#     timeofday = timeofday + timedelta(hours=8)
#     return timeofday
def timestamp_to_timeofday(timestamp):
    microseconds_since_epoch = timestamp

    # 计算秒数和微秒数
    seconds_since_epoch = microseconds_since_epoch // 1_000_000
    remaining_microseconds = microseconds_since_epoch % 1_000_000

    # 使用 timedelta 和 datetime 将秒数转换为具体的日期和时间
    timeofday = datetime(1970, 1, 1) + timedelta(seconds=seconds_since_epoch)
    # 将时间转换为东八区时间
    timeofday = timeofday + timedelta(hours=8)

    # 格式化时间字符串，精确到微秒
    formatted_time = timeofday.strftime("%Y-%m-%d %H:%M:%S") + ".%06d" % remaining_microseconds

    return formatted_time

def show_data(influx, data):
    if (influx['table_name'] == "Voltage"):
        print("===========================================================")
    prefix=influx['mac_address'] + " " + timestamp_to_timeofday(influx['start_timestamp']) + " " +influx['table_name']+ ":"
    print(prefix, end='')

    if (influx['table_name'] == "waveform_Voltage"):
        print("===Waveform data: see waveform.txt ...")
        with open("waveform.txt", "a") as file:
            line = ' '.join(str(value) for value in data) + "\n"  # 将数据列表转换为字符串，并在每个数据之间添加空格
            file.write(line)  # 写入一行数据到文件
    else:
        for value in data:
            print(" ",str(value))


def show_waveform(influx, data):
    if (influx['table_name'] == "waveform_Current"):
        prefix=influx['mac_address'] + " " + timestamp_to_timeofday(influx['start_timestamp']) + " " +influx['table_name']+ ":"
        print(prefix, end='')
        print("===Waveform data: see waveform.txt ...")

        with open("waveform.txt", "a") as file:
            line = ' '.join(str(value) for value in data) + "\n"  # 将数据列表转换为字符串，并在每个数据之间添加空格
            file.write(line)  # 写入一行数据到文件


