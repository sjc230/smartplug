# Please use python language to complete the code for the following requirements:
# It is necessary to remotely control the switch of a socket through mqtt, and it is required to 
#   prompt the user to enter a control command interactively in the terminal of the system.
# First, the user is requested to enter the ID number of the switch as the MQTT topic, 
#   and then the switch command is input. After receiving the command input by the user, 
#   the command is sent through mqtt with a Qos=1 message.
# Then wait for the execution result command to be sent back remotely. 
#   The topic of the command is the ID number + "result", and the payload is the execution result. 
#   After receiving the return command, the result is printed. If the execution result is not received 
#   for more than 10 seconds, timeout information will be output and the wait will end.
# After completing such a complete interaction, re-enter the waiting state for the next round of interaction.

import paho.mqtt.client as mqtt
import time
import pandas as pd
from pathlib import Path

# Set path to local directory
p = Path('.')
#file_path = Path.is_file("plug_groups.csv")

# Create list of grops
group_list = []

# Read in groups if they exist
"""
if file_path.is_file():
        print("No groups are setup.")
    else:
        with file_path.open() as f:
            for line in f:
                line_as_string = line.rstrip('\n')  # Remove trailing newline
                g_list = line_as_string.split(",")
                group_list.append(g_list)
"""

# GROUP LIST FORMAT
# [group name, group ON time, group OFF time, 1st plug MAC, ... , last plug MAC]                

def add_group():
    print("place holder")
    return list

def delete_group():
    print("place holder")
    return list

def add_to_group():
    print("place holder")
    return list

def remove_from_group():
    print("place holder")
    return list

def set_group_ontime():
    print("place holder")
    return list

def set_group_offtime():
    print("place holder")
    return list

def write_lists_csv():
    # Clear content of csv file
    with file_path.open('w') as f:
        pass
    # Write current group content to csv file
    pd.to_csv("plug_groups.csv")
    return

# MQTT Broker Address
broker_address = "sensorwebdata.engr.uga.edu" #"sensorweb.us"
# broker_address = "122.152.204.216"
# MQTT Broker Port
broker_port = 1883 #8883
# MQTT Broker Username
broker_username = "aideveloper" #"algtest"
# broker_username = "smart_test"
# MQTT Broker Password
broker_password = "aidev@122" #"sensorweb711"
# broker_password = "test777"
# MQTT Subscribe to topic
sub_topic = ""
control_topic=""

message_received = False

# Define MQTT Client
client = mqtt.Client()

# Connect MQTT Broker
client.username_pw_set(username=broker_username, password=broker_password)
# client.connect(broker_address, broker_port)

# MQTT Message callback function
def on_message(client, userdata, message):
    global message_received
    print("execution feedback：", message.topic, "="+str(message.payload.decode()))
    message_received = True

# Set message callback function
client.on_message = on_message


# issue control commands
def publish_command(topic, command):
    client.publish(topic, command, qos=2)
    

# main loop
while True:
    print("\r\n=====Start Controling your SmartPowerPlug Remotly=====")
    # User enters device ID
    device_id = input("Please Input MAC Address of SmartPP：")

    if len(device_id) > 0 :
        control_topic="/SPP_relay/" + device_id.upper()
        sub_topic = "/SPP_relay_status/" + device_id.upper()
    else:
        control_topic="/SPP_relay/#" 
        sub_topic = "/SPP_relay_status/#"

    # User input control command
    command = input("Control Command(on/off/status):")

    client.connect(broker_address, broker_port)
    # Subscribe to results topic
    client.subscribe(sub_topic)

    message_received = False
    # issue control commands
    publish_command(control_topic, command)

    # Wait for execution results
    start_time = time.time()
    while not message_received:
        if time.time() - start_time > 15:
            print("Execution result not received after timeout。")
            break
        client.loop(timeout=1.0)

    client.unsubscribe(sub_topic)
    # Reset message receiving flag
    message_received = False
    # Disconnect after completing this interaction
    client.disconnect()

