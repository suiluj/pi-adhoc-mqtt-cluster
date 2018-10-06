import gyro # pylint: disable=E0401
import time
import json

# debug
import pprint

from mqtthandler import Mqtthandler

lage_speed = 1
device = "zpi1"
sensor = "mpu6050"

class Lagesensor(Mqtthandler):
    def on_message(self,mosq, obj, msg):
        print('Nachricht empfangen.')



def getpayloaddatanew():
    fields = gyro.winkel()
    return fields
  

service = Lagesensor(service_name='Lagesensor',service_description='Lagesensor Wert wird geschickt')


# for functions with arguments
# getpayloadfunction_arguments = {"pitch":5.0,"roll":4.0}
# last parameter only when get data needs args
# service.add_publish('data/' + service.service_path + '/lage',1,getpayloaddatanew,getpayloadfunction_arguments)


# for publish without argument
# service.add_publish('data/' + service.service_path + '/lage',0.3,getpayloaddatanew)


# for measurement without argument

measurement_influxdb_name = "lage"
measurement = {
    "measurement_name" : "Lagesensor am zpi1",
    "measurement_influxdb_name" : measurement_influxdb_name,
    "measurement_id" : service.service_id + "---" + measurement_influxdb_name,
    "measurement_tags" : {
        "device_name": service.device_name.replace(':','-').replace(' ', '_').lower(),
        "device_id": service.device_id.replace(':','-').replace(' ', '_').lower(),
        "service_name": service.service_name.replace(':','-').replace(' ', '_').lower(),
        "service_id": service.service_id.replace(':','-').replace(' ', '_').lower(),
        "sensor": "mpu6050".replace(':','-').replace(' ', '_').lower(),
    },
    "measurement_fields" : [
        {
            "measurement_field_name" : "Pitch-Achse",
            "measurement_field_id" : "pitch",
            "measurement_field_unit" : "Degree",
        },
        {
            "measurement_field_name" : "Roll-Achse",
            "measurement_field_id" : "roll",
            "measurement_field_unit" : "Degree",
        },
    ]
}

# better for future extra parameter for measurement influxdb name , measurement name and fields alone, all the rest is standard in class
service.add_measuremet(service.service_path + '/data/' + measurement_influxdb_name,0.1,getpayloaddatanew,measurement)

# idea: interval als self.dict oder array nachträglich veränderbar und es wird nur der key übergeben automatisch key subscribe erstellen.

# service.add_subscribe("info/#", 1)

# pprint.pprint(service.mqtt_host)

service.start_mqtt(loopforever=True)
