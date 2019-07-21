# pylint: disable=E0401
# from gpiozero import MCP3008,LED
# phototransistor with 10k ohm; lm335 with 1.2k ohm
from gpiozero import MCP3008
from mqtthandler import Mqtthandler

class ADCSensor(Mqtthandler):
    def on_message(self,mosq, obj, msg):
        print('Nachricht empfangen.')


def getpayload_temperature():
    measurevoltage_percent = sensortemp.value
    refvoltage = 3.3
    degree_celcius = (refvoltage * measurevoltage_percent / 1.0 * 100.0) - 273.15

    fields = {
        "degree_celcius" : degree_celcius
    }
    return fields


def getpayload_brightness():
    measurevoltage_percent = sensorbrithness.value
    # refvoltage = 3.3

    fields = {
        "brightness_percent" : measurevoltage_percent
    }
    return fields
  


sensortemp = MCP3008(0) # sensortemp is connected to CH0
sensorbrithness = MCP3008(1) # sensorbrithness is connected to CH1

service = ADCSensor(service_name='ADC Sensoren',service_description='Sensoren am MCP3008 Digital Analog Wandler')


measurement_influxdb_name = "temperature"
measurement = {
    "measurement_name" : "Temperatur lm335 am zpi2",
    "measurement_influxdb_name" : measurement_influxdb_name,
    "measurement_id" : service.service_id + "---" + measurement_influxdb_name,
    "measurement_tags" : {
        "device_name": service.device_name.replace(':','-').replace(' ', '_').lower(),
        "device_id": service.device_id.replace(':','-').replace(' ', '_').lower(),
        "service_name": service.service_name.replace(':','-').replace(' ', '_').lower(),
        "service_id": service.service_id.replace(':','-').replace(' ', '_').lower(),
        "sensor": "lm335".replace(':','-').replace(' ', '_').lower(),
    },
    "measurement_fields" : [
        {
            "measurement_field_name" : "Temperatur Grad Celcius",
            "measurement_field_id" : "degree_celcius",
            "measurement_field_unit" : "Degree Celcius",
        },
        
    ]
}

service.add_measuremet(service.service_path + '/data/' + measurement_influxdb_name,2,getpayload_temperature,measurement)

measurement_influxdb_name = "brightness"
measurement = {
    "measurement_name" : "Helligkeit LPT 80 am zpi2",
    "measurement_influxdb_name" : measurement_influxdb_name,
    "measurement_id" : service.service_id + "---" + measurement_influxdb_name,
    "measurement_tags" : {
        "device_name": service.device_name.replace(':','-').replace(' ', '_').lower(),
        "device_id": service.device_id.replace(':','-').replace(' ', '_').lower(),
        "service_name": service.service_name.replace(':','-').replace(' ', '_').lower(),
        "service_id": service.service_id.replace(':','-').replace(' ', '_').lower(),
        "sensor": "LPT 80".replace(':','-').replace(' ', '_').lower(),
    },
    "measurement_fields" : [
        {
            "measurement_field_name" : "Helligkeit Prozent",
            "measurement_field_id" : "brightness_percent",
            "measurement_field_unit" : "percent",
        },
        
    ]
}

service.add_measuremet(service.service_path + '/data/' + measurement_influxdb_name,0.2,getpayload_brightness,measurement)


service.start_mqtt(loopforever=True)
