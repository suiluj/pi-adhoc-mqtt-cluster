# -*- coding: utf-8 -*-
import time
import json

from influxdb import InfluxDBClient
from collections import deque

from mqtthandler import Mqtthandler

class Mqttinfluxdbhandler(Mqtthandler):
    def on_message(self,mosq, obj, msg):
        global pointsdeque
        
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

    
def write_to_influxdb():
    global write_db_speed
    global pointsdeque

    sendpointslist = []

    while True:
        try:
            sendpointslist.append(pointsdeque.popleft())   
        except IndexError:
            break



    client.write_points(sendpointslist,time_precision='ms')
    return {"datapoints_topics_all" : len(sendpointslist)}



pointsdeque = deque()
write_db_speed = 1

service = Mqttinfluxdbhandler(service_name='MQTT To InfluxDB',service_description='Speichert alle measurement data MQTT Nachrichten in die InfluxDB Datenbank')

service.add_subscribe("+/+/data/#", 1)

measurement_influxdb_name = "mqtt_to_influxdb"
measurement = {
    "measurement_name" : "Written Data Points to InfluxDB",
    "measurement_influxdb_name" : measurement_influxdb_name,
    "measurement_id" : service.service_id + "---" + measurement_influxdb_name,
    "measurement_tags" : {
        "device_name": service.device_name.replace(':','-').replace(' ', '_').lower(),
        "device_id": service.device_id.replace(':','-').replace(' ', '_').lower(),
        "service_name": service.service_name.replace(':','-').replace(' ', '_').lower(),
        "service_id": service.service_id.replace(':','-').replace(' ', '_').lower(),
        "script": "mqttdatatoinfluxdb".replace(':','-').replace(' ', '_').lower(),
    },
    "measurement_fields" : [
        {
            "measurement_field_name" : "Alle Datenpunkte Topics",
            "measurement_field_id" : "datapoints_topics_all",
            "measurement_field_unit" : "Number per Database Write Action",
        },
    ]
}

# better for future extra parameter for measurement influxdb name , measurement name and fields alone, all the rest is standard in class
service.add_measuremet(service.service_path + '/data/' + measurement_influxdb_name,write_db_speed,write_to_influxdb,measurement)




client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('mqtt_python')

service.start_mqtt(loopforever=True)
