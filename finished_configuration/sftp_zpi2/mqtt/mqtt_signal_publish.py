# MQTT Publish Demo
# Publish two messages, to two different topics


import math
import sched
import time

import paho.mqtt.publish as publish

s = sched.scheduler(time.time, time.sleep)

# host = "192.168.2.101"  # lan zu hause
# host = "192.168.43.15"  # lan handy hotspot
host = "1.0.0.1"  # lan allgemeint falls hostname geht
portnumber = 1883

# host = "juliusheine.de"  # lan allgemeint falls hostname geht
# portnumber = 65102

def do_something(sc):
    t = time.time() - starttime
    # x = math.sin(2 * math.pi * t)
    # x = math.sin(t)
    x = round(math.sin(t),2)
    print('Signal ', x)
    publish.single("Signal", x, hostname=host, port=portnumber)
    # publish.single("CoreElectronics/test", "Hello", hostname="192.168.2.101")
    # publish.single("CoreElectronics/topic", "World!", hostname="192.168.2.101")
    # print("Signal gesendet")
    s.enter(0.5, 1, do_something, (sc,))


s.enter(0, 1, do_something, (s,))

starttime = time.time()

s.run()

