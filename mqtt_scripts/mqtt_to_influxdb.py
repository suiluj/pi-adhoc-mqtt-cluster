#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# All rights reserved.

# This shows a simple example of an MQTT subscriber using a per-subscription message handler.

# import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import time
import json
from influxdb import InfluxDBClient
import sched
import socket
import fcntl
import struct

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

from collections import deque

# device_name = socket.gethostname()
device_name = '3pi1.local'
# device_id = getHwAddr('wlan0')
device_id = str('b8:27:eb:77:3d:37')
service_name = "MQTT To InfluxDB"
service_id = str(device_id + "-" + service_name).replace(':','-').replace(' ', '_').lower()
service_description = "Save MQTT messages to the InfluxDB database"

client = InfluxDBClient(host=device_name, port=8086)
client.switch_database('mqtt_python')

mqtthostname = device_name

s = sched.scheduler(time.time, time.sleep)

write_db_speed = 1
publish_info_topic_speed = 1


topics_published = [
    'info/' + device_id + '/' + service_id + '/info',
    'data/' + device_id + '/' + service_id + '/lage',
    
]

topics_subscribed = [
    'write_db_speed',
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

pointsdeque = deque()

# def on_message_msgs(mosq, obj, msg):
#     # This callback will only be called for messages with topics that match
#     # $SYS/broker/messages/#
#     print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# def on_message_bytes(mosq, obj, msg):
#     # This callback will only be called for messages with topics that match
#     # $SYS/broker/bytes/#
#     print("BYTES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_message(mosq, obj, msg):
    global pointsdeque
    # This callback will be called for messages that we receive that do not
    # match any patterns defined in topic specific callbacks, i.e. in this case
    # those messages that do not have topics $SYS/broker/messages/# nor
    # $SYS/broker/bytes/#
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    time_received_msvalue = int(time.time()*1000)
    message_json = json.loads(msg.payload.decode('utf-8'))
    message_json['fields']['time_received_msvalue'] = time_received_msvalue
    message_json['fields']['delay_received_msvalue'] = time_received_msvalue - message_json['timemsvalue']
    pointsdeque.append(
          {
            "measurement": message_json['measurement'],
            "tags": message_json['tags'],
            "time": message_json['timemsvalue'],
            "fields": message_json['fields'],
        }
    )
    # test
    # print(int(time.time()*1000))
    
mqttc = mqtt.Client(client_id=service_id)

# Add message callbacks that will only trigger on a specific subscription match.
# mqttc.message_callback_add("$SYS/broker/messages/#", on_message_msgs)
# mqttc.message_callback_add("$SYS/broker/bytes/#", on_message_bytes)
mqttc.on_message = on_message
mqttc.connect(mqtthostname, 1883, 60)

# mqttc.subscribe("$SYS/#", 0)


# mqttc.subscribe([("wetter", 1)])
# mqttc.subscribe([("lage", 1)])
# mqttc.subscribe([("lage", 1),("wetter", 1)])
mqttc.subscribe("+/+/data/#", 1)

mqttc.loop_start()

def publish_info_topic(sc):
    global publish_info_topic_speed
    global info_topic_dict

    mqttc.publish(topics_published[0], json.dumps(info_topic_dict), qos=1)

    s.enter(float(publish_info_topic_speed), 1, publish_info_topic, (sc,))

def write_to_influxdb(sc):
    global write_db_speed
    global pointsdeque

    sendpointslist = []

    while True:
        try:
            sendpointslist.append(pointsdeque.popleft())   
        except IndexError:
            break



    client.write_points(sendpointslist,time_precision='ms')

    s.enter(float(write_db_speed), 1, write_to_influxdb, (sc,))


# write to db loop
s.enter(0, 1, write_to_influxdb, (s,))

# publish info topic loop
s.enter(0, 2, publish_info_topic, (s,))

s.run()