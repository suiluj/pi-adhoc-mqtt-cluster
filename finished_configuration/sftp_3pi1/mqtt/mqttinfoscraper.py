# -*- coding: utf-8 -*-
import time
import json
import redis

from mqtthandler import Mqtthandler

class Mqttinfotopics(Mqtthandler):
    def on_message(self,mosq, obj, msg):
        # This callback will be called for messages that we receive that do not
        # match any patterns defined in topic specific callbacks, i.e. in this case
        # those messages that do not have topics $SYS/broker/messages/# nor
        # $SYS/broker/bytes/#
        # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        # time_received_msvalue = int(time.time()*1000)
        message_json = json.loads(msg.payload.decode('utf-8'))

        # pprint.pprint(message_json)
        # message_json['time_last_info_msvalue'] = time_received_msvalue

        # self.services[message_json['service_id']] = message_json
        # # redisClient.set('services', json.dumps(self.services).encode('utf-8'))
        key = message_json['service_id']
        value = message_json
        mydict = {}
        mydict[key] = value
        redisClient.hmset("services", mydict)
        # print(message_json['service_id'])
        # print(message_json)

    

service = Mqttinfotopics(service_name='Get Info Topics',service_description='Sammelt alle Info-Topics um sie fuer (Umlaute noch nicht unterstuetzt) dieses Dashboard bereitszustellen')

service.add_subscribe("+/+/info/#", 1)

redisClient = redis.StrictRedis(host='127.0.0.1',port=6379)

service.start_mqtt(loopforever=True)
