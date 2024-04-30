# 请用python语言完成如下需求的代码：
# 需要通过mqtt远程控制一个插座的开关，要求可以系统的terminal中提示用户输入控制命令交互来控制。
# 首先向用户请求输入开关的ID号作为MQTT的topic，然后输入开关命令，接收到用户输入的命令后则将该命令通过mqtt发送Qos=1的消息。
# 接着等待远程发回执行结果命令，该命令的topic为ID号+“result”，payload为执行结果，接收到返回命令后打印输出结果。若超过10秒未收到执行结果，则输出超时信息并结束等待。
# 结束如此一次完整的交互后，重新进入等待下一轮交互状态。

import paho.mqtt.client as mqtt
import time

# MQTT Broker 地址
broker_address = "sensorweb.us"
# broker_address = "122.152.204.216"
# MQTT Broker 端口
broker_port = 1883
# MQTT Broker 用户名
broker_username = "algtest"
broker_username = "smart_test"
# MQTT Broker 密码
broker_password = "sensorweb711"
# broker_password = "test777"
# MQTT 订阅主题
sub_topic = ""
control_topic=""

message_received = False

# 定义 MQTT 客户端
client = mqtt.Client()

# 连接 MQTT Broker
client.username_pw_set(username=broker_username, password=broker_password)
# client.connect(broker_address, broker_port)

# MQTT 消息回调函数
def on_message(client, userdata, message):
    global message_received
    print("execution feedback：", message.topic, "="+str(message.payload.decode()))
    message_received = True

# 设置消息回调函数
client.on_message = on_message


# 发布控制命令
def publish_command(topic, command):
    client.publish(topic, command, qos=2)
    

# 主循环
while True:
    print("\r\n=====Start Controling your SmartPowerPlug Remotly=====")
    # 用户输入设备 ID
    device_id = input("Please Input MAC Address of SmartPP：")

    if len(device_id) > 0 :
        control_topic="/SPP_relay/" + device_id.upper()
        sub_topic = "/SPP_relay_status/" + device_id.upper()
    else:
        control_topic="/SPP_relay/#" 
        sub_topic = "/SPP_relay_status/#"

    # 用户输入控制命令
    command = input("Control Command(on/off/status):")

    client.connect(broker_address, broker_port)
    # 订阅结果主题
    client.subscribe(sub_topic)

    message_received = False
    # 发布控制命令
    publish_command(control_topic, command)

    # 等待执行结果
    start_time = time.time()
    while not message_received:
        if time.time() - start_time > 15:
            print("超时未收到执行结果。")
            break
        client.loop(timeout=1.0)

    client.unsubscribe(sub_topic)
    # 重置消息接收标志
    message_received = False
    # 结束本次交互后断开连接
    client.disconnect()

