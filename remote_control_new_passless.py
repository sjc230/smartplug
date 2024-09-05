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

# MQTT Broker address
broker_address = "sensorweb.us"
# broker_address = "122.152.204.216"
# MQTT Broker port
broker_port = 1883
# MQTT Broker username
broker_username = ""
# broker_username = "smart_test"
# MQTT Broker password
broker_password = ""
# broker_password = "test777"
# MQTT subscription topic
sub_topic = ""
control_topic = ""

message_received = False

# Define MQTT client
client = mqtt.Client()

# Connect to MQTT Broker
if broker_password != "" and broker_username != "":
    client.username_pw_set(username=broker_username, password=broker_password)
# client.connect(broker_address, broker_port)

# MQTT message callback function
def on_message(client, userdata, message):
    global message_received
    print("execution feedback:", message.topic, "=" + str(message.payload.decode()))
    message_received = True

# Set the message callback function
client.on_message = on_message


# Publish control command
def publish_command(topic, command):
    client.publish(topic, command, qos=2)


# Main loop
while True:
    print("\r\n=====Start Controlling your SmartPowerPlug Remotely=====")
    # User inputs the device ID
    device_id = input("Please Input MAC Address of SmartPP:")

    if len(device_id) > 0:
        control_topic = f"/smartPP_org_name/{device_id.lower()}/SPP_relay"
        sub_topic = f"/smartPP_org_name/{device_id.lower()}/SPP_relay_status"
    else:
        control_topic = "/+/+/SPP_relay"
        sub_topic = "/+/+/SPP_relay_status"

    # User inputs control command
    command = input("Control Command(on/off/status):")

    client.connect(broker_address, broker_port)
    # Subscribe to result topic
    client.subscribe(sub_topic)

    message_received = False
    # Publish control command
    publish_command(control_topic, command)

    # Wait for execution result
    start_time = time.time()
    while not message_received:
        if time.time() - start_time > 15:
            print("Timeout: No execution result received.")
            break
        client.loop(timeout=1.0)

    client.unsubscribe(sub_topic)
    # Reset the message received flag
    message_received = False
    # Disconnect after completing this interaction
    client.disconnect()