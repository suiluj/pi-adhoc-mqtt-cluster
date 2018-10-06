import paho.mqtt.client as mqtt
import json
import time

import socket
import fcntl
import struct

import threading

def get_mac_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname[:15], 'utf-8')))
    return ''.join(['%02x:' % b for b in info[18:24]])[:-1]

class Mqtthandler:

    def __init__(self, service_name=None,service_description=None,mqtt_host='localhost',mqtt_port=1883,device_name=None,device_id=None):

        self.service_name = service_name
        self.service_description = service_description

        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port

        if device_name is None:
            self.device_name = socket.gethostname()
        else:
            self.device_name = device_name

        if device_id is None:
            self.device_id = get_mac_addr('wlan0')
        else:
            self.device_id = device_id

        self.service_id = str('service-' + self.device_id + "-" + self.service_name).replace(':','-').replace(' ', '_').lower()

        self.service_path = str(self.device_id).replace(':','-').replace(' ', '_').lower() + '/' + self.service_id

        self.topics_published = []

        # default subscribed topic
        self.topics_subscribed = []

        # empty list will be filled via add measurement method
        self.measurements = {}

        # default one second; will be changed via mailbox messages
        self.publish_info_topic_speed = 1

        self.mqttc = mqtt.Client(client_id=self.service_id)

        # will be sent every second
        self.info_topic_dict = {
            "service_name" : self.service_name,
            "service_description" : self.service_description,
            "service_id" : self.service_id,
            "device_name" : self.device_name,
            "device_id" : self.device_id,
            "service_path" : self.service_path,
            "service_start_time" : int(time.time()*1000),
            "topics_published" : self.topics_published,
            "topics_subscribed" : self.topics_subscribed,
            "measurements" : self.measurements
        }

        # empty list of threads will be filled with info topic and topic publish threads via start and add publish methods
        self.threads = []
        self.lock = threading.Lock()

        self.counter_thread = 0
        self.counter_publish = 0
        self.couter_measurement = 0

        

    def on_connect(self,client, userdata, flags, rc):
        self.mqttc.subscribe(self.topics_subscribed)
        
        for t in self.threads:
            t.start()

    def on_message(self,mosq, obj, msg):
        # overwrite this method in the mqtthandlerchildclass where mqtthandler is parent
        # This callback will be called for messages that we receive that do not
        # match any patterns defined in topic specific callbacks, i.e. in this case
        # those messages that do not have topics $SYS/broker/messages/# nor
        # $SYS/broker/bytes/#
        # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        print('Message received. Overwrite  on_message(self,mosq, obj, msg): in child class')

    def publish_data_loop(self,publish_topic,publish_interval,getpayloadfunction_name,measurement,getpayloadfunction_arguments):
        while True:
            self.lock.acquire()
            # print('Sending: {}'.format(publish_topic))
            
            if getpayloadfunction_arguments is None:
                payloaddata = getpayloadfunction_name()
            else:
                payloaddata = getpayloadfunction_name(**getpayloadfunction_arguments)
            
            if measurement is None:
                message_data = json.dumps(payloaddata)
            else:
                message_dict = {
                    "measurement" : measurement['measurement_influxdb_name'],
                    "fields" : payloaddata,
                    "timemsvalue" : int(time.time()*1000),
                    "tags" : measurement['measurement_tags'],
                }
                message_data = json.dumps(message_dict)

            self.mqttc.publish(publish_topic,message_data,qos=1)
            self.lock.release()
            # statt festem publish interval hier index eines arrays mit variablen self intervalen übergeben, so kann das sende interval später noch angepasst werden
            time.sleep(publish_interval)

    def add_publish(self,publish_topic,publish_interval,getpayloadfunction_name,measurement=None,getpayloadfunction_arguments=None):
        t = threading.Thread(target=self.publish_data_loop, args=(publish_topic,publish_interval,getpayloadfunction_name,measurement,getpayloadfunction_arguments))
        t.daemon = True
        self.threads.append(t)
        self.topics_published.append(publish_topic)


    def add_measuremet(self,publish_topic,publish_interval,getpayloadfunction_name,measurement,getpayloadfunction_arguments=None):
        self.add_publish(publish_topic,publish_interval,getpayloadfunction_name,measurement,getpayloadfunction_arguments)
        self.measurements[measurement['measurement_id']] = measurement

    def add_subscribe(self,topic,qos=1):
        new_subscribe = (topic, qos)
        self.topics_subscribed.append(new_subscribe)


    def start_mqtt(self,loopforever=False):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        
        
        # self.mqttc.subscribe(self.topics_subscribed)
        
        self.add_publish(self.service_path + '/info',self.publish_info_topic_speed,self.getinfotopicdict)

        self.add_subscribe(self.service_path + '/mailbox',1)

        self.mqttc.connect(self.mqtt_host, self.mqtt_port, 60)


        if loopforever is True:
            self.mqttc.loop_forever()
        else:
            self.mqttc.loop_start()

    def getinfotopicdict(self):
        latest_info_topic_dict = self.info_topic_dict
        latest_info_topic_dict["time_last_info_msvalue"] = int(time.time()*1000)
        return latest_info_topic_dict
    
