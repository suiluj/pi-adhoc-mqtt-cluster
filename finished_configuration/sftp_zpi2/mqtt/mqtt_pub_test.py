# MQTT Publish Demo
# Publish two messages, to two different topics


import math
import sched
import time
from random import randint
# print(randint(0, 9))


import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

current_milli_time = lambda: int(round(time.time() * 1000))

host = "localhost"  # lan zu hause
# host = "192.168.2.101"  # lan zu hause
# host = "192.168.43.15"  # lan handy hotspot
# host = "raspberrypi"  # lan allgemeint falls hostname geht
# host = "10.3.141.1"  # rpiap hotspot
portnumber = 1883

# uberspace
# host = "juliusheine.de"  
# portnumber = 65102


dice_speed = 1

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("dice_speed")
    # client.subscribe("CoreElectronics/topic")
    # client.subscribe("CoreElectronics/topic")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global dice_speed
    # print(msg.topic + " " + str(msg.payload))
    print(msg.topic + ": " + msg.payload.decode("utf-8"))

    dice_speed = msg.payload.decode("utf-8")


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
testspeed = 0.5


def do_something(sc):
    #global dice_speed
    #x = randint(1, 6)
    #print('Es wurde eine ', x, 'gewürfelt. Senden...')
    #publish.single("Wuerfel", x, hostname=host, port=portnumber)
    x = current_milli_time()
    publish.single("test", x, qos=1, hostname=host, port=portnumber)
    
    
    # publish.single("CoreElectronics/test", "Hello", hostname="192.168.2.101")
    # publish.single("CoreElectronics/topic", "World!", hostname="192.168.2.101")
    #print("Gesendet.")

    s.enter(2, 1, do_something, (sc,))


s.enter(0, 1, do_something, (s,))

starttime = time.time()

s.run()

