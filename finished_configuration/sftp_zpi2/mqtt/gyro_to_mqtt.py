import gyro # pylint: disable=E0401
# import time

# while True:
#     print(gyro.winkel())
#     time.sleep(1)

# MQTT Publish Demo
# Publish two messages, to two different topics

# import math
import sched
import time
import json

import socket
import fcntl
import struct

def get_mac_addr(ifname):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname[:15], 'utf-8')))
  return ''.join(['%02x:' % b for b in info[18:24]])[:-1]

# from random import randint
# print(randint(0, 9))

# import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

# host = "192.168.2.101"  # lan zu hause
host = "localhost"  # localhost
# host = "192.168.43.15"  # lan handy hotspot
# host = "raspberrypi"  # lan allgemeint falls hostname geht
# host = "10.3.141.1"  # rpiap hotspot
portnumber = 1883
device = "zpi1"
sensor = "mpu6050"
# uberspace
# host = "juliusheine.de"  
# portnumber = 65102


lage_speed = 1



device_name = socket.gethostname()
# device_name = '3pi1.local'
device_id = get_mac_addr('wlan0')
# device_id = str('b8:27:eb:77:3d:37')
service_name = "Lagesensor"
service_id = str(device_id + "-" + service_name).replace(':','-').replace(' ', '_').lower()
service_description = "Send position sensor data via MQTT"

publish_info_topic_speed = 1


topics_published = [
    'info/' + device_id + '/' + service_id + '/info',
    'data/' + device_id + '/' + service_id + '/lage',
    
]

topics_subscribed = [
    'lage_speed',
    'write_info_topic_speed',
]

timemsvalue = int(time.time()*1000)
# timemsvalue = (ntptime.time() + 946684800)*1000 + (utime.ticks_ms()% 1000)
measurement = 'lage'
# message_dict = {"measurement" : measurement, "fields" : fields, "timemsvalue": timemsvalue}
info_topic_dict = {
    "service_name" : service_name,
    "service_description" : service_description,
    "service_id" : service_id,
    "device_id" : device_id,
    "service_start_time" : timemsvalue,
    "topics_published" : topics_published,
    "topics_subscribed" : topics_subscribed,
}



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("lage_speed")
    # client.subscribe("CoreElectronics/topic")
    # client.subscribe("CoreElectronics/topic")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global lage_speed
    # print(msg.topic + " " + str(msg.payload))
    print(msg.topic + ": " + msg.payload.decode("utf-8"))

    lage_speed = msg.payload.decode("utf-8")


# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host, portnumber, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_start()


s = sched.scheduler(time.time, time.sleep)
# testspeed = 0.5



def publish_info_topic(sc):
    global publish_info_topic_speed
    global info_topic_dict

    client.publish(topics_published[0], json.dumps(info_topic_dict), qos=1)

    s.enter(float(publish_info_topic_speed), 1, publish_info_topic, (sc,))


def do_something(sc):
    global lage_speed
    global device
    global sensor
    # x = randint(1, 6)
    # print('Es wurde eine ', x, 'gewürfelt. Senden...')


    # await asyncio.sleep_ms(1000)
    tags = {
        "device" : device,
        "sensor": sensor,
    }
    fields = gyro.winkel()
    timemsvalue = int(time.time()*1000)
    # timemsvalue = (ntptime.time() + 946684800)*1000 + (utime.ticks_ms()% 1000)
    measurement = 'lage'
    # message_dict = {"measurement" : measurement, "fields" : fields, "timemsvalue": timemsvalue}
    message_dict = {
        "measurement" : measurement,
        "fields" : fields,
        "timemsvalue" : timemsvalue,
        "tags" : tags,
    }

    # print('publish', data)
    # If WiFi is down the following will pause for the duration.
    # await client.publish('wetter', '{}'.format(json.dumps(data)), qos = 1)

# achtung besser über client machen wahrscheinlich, dann auch qos 1 geht bestimmt
# client.publish(....
# http://www.steves-internet-guide.com/into-mqtt-python-client/
    client.publish("data/lage", json.dumps(message_dict), qos=1)
    # publish.single("CoreElectronics/test", "Hello", hostname="192.168.2.101")
    # publish.single("CoreElectronics/topic", "World!", hostname="192.168.2.101")
    print("Gesendet.")

    s.enter(float(lage_speed), 1, do_something, (sc,))


s.enter(0, 1, do_something, (s,))


# publish info topic loop
s.enter(0, 2, publish_info_topic, (s,))

starttime = time.time()

s.run()
