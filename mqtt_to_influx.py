import paho.mqtt.client as mqtt
import threading
from utils import write_influx, get_config_info, write_influx_test,show_data,show_waveform,timestamp_to_timeofday
from write_to_excel import write_to_excel_db #write_to_excel #write_to_csv 
import struct


config_info ={}

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

    for topic in config_info["topic_mapping"].keys():
        client.subscribe(topic,qos=1)


def parse_beddot_data(bytedata):

    mac_addr = ":".join(f"{x:02x}" for x in struct.unpack("!BBBBBB", bytedata[0:6]))
    data_len =struct.unpack("H",bytedata[6:8])[0]
    timestamp=struct.unpack("L",bytedata[8:16])[0]  # in micro second
    data_interval=struct.unpack("I",bytedata[16:20])[0]  # in micro second

    # data=[0]*int((len(bytedata)-20)/4)
    data=[0]*data_len
    index=20
    for i in range(data_len):
        if len(bytedata[index:index+4]) == 4:
            data[i] = struct.unpack("i", bytedata[index:index+4])[0]
            index +=4
    # print("mac_addr,",mac_addr,timestamp,data_interval)
    return mac_addr, timestamp, data_interval, data


from datetime import datetime, timedelta
def print_timestamp(timestamp):
    microseconds_since_epoch = timestamp
    seconds_since_epoch = microseconds_since_epoch // 1_000_000

    # 使用 timedelta 和 datetime 将秒数转换为具体的日期和时间
    timestamp = datetime(1970, 1, 1) + timedelta(seconds=seconds_since_epoch)
    print(f"The timestamp is: {timestamp}")

def assemble_influx_package(topic, mac_addr, timestamp, data_interval):
    returnDict = {}

    if topic in config_info["topic_mapping"].keys():
        returnDict["db_name"] = config_info["topic_mapping"][topic]["database"]
        returnDict["table_name"] = config_info["topic_mapping"][topic]["db_table"]
        returnDict["data_name"]  = config_info["topic_mapping"][topic]["dataname"]
        # returnDict["data"] = data
        returnDict["mac_address"] = mac_addr
        returnDict["start_timestamp"] = timestamp
        returnDict["interval"] = data_interval

        returnDict["ip"] = config_info["influx_ip"]
        returnDict["user"] = config_info["influx_user"]
        returnDict["passw"] = config_info["influx_pass"]
    # print(returnDict)
    return returnDict

def log_data_to_file(influx, data):
    filename=influx['mac_address'] + ".xlsx"
    timestamp=timestamp_to_timeofday(influx['start_timestamp'])
    field=influx['table_name']
    
    for value in data:
        write_to_excel_db(filename, timestamp, field, value)
        timestamp = timestamp_to_timeofday(influx['start_timestamp'] + influx['interval'])

# def log_data_to_file(influx, data):
#     # 定义线程函数, launch a new thread to handle saving data to an excel file asynchonously
#     def thread_function():
#         filename=influx['mac_address'] + ".xlsx"
#         timestamp=timestamp_to_timeofday(influx['start_timestamp'])
#         field=influx['table_name']

#         for value in data:
#             write_to_excel_db(filename, timestamp, field, value)
#             timestamp = timestamp_to_timeofday(influx['start_timestamp'] + influx['interval'])

#     # 启动线程
#     thread = threading.Thread(target=thread_function)
#     thread.start()


def on_message(client, userdata, msg):
    # print(f"Received message: {msg.topic}")

    # if (msg.topic == "geophone") or (msg.topic=="batter_volt") or (msg.topic=="usb_volt"):
    #     return
    # get payload data
    payload_bytes = msg.payload

    # print("payload len:", len(payload_bytes))
    # hex_string = ' '.join([hex(b) for b in payload_bytes])
    # print(hex_string)

    mac_addr, timestamp, data_interval, data=parse_beddot_data(payload_bytes)
    # print_timestamp(timestamp)
    influx_info=assemble_influx_package(msg.topic, mac_addr,timestamp, data_interval)

    # write_influx(influx_info, data)
    # show_data (influx_info, data)
    log_data_to_file (influx_info, data)
    # show_waveform(influx_info, data)

    
if __name__ == '__main__':

    config_info = get_config_info() 
    broker = config_info["broker"]
    port = config_info["port"]
    print("broker =",broker, "port=",port)
    print(config_info)
    # Create MQTT client
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(broker, port, 60)

    mqtt_thread = threading.Thread(target=client.loop_forever())
    mqtt_thread.start()
