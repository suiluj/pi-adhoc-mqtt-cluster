# pi-adhoc-mqtt-cluster
Using batman-adv to connect several raspberrypi to a mesh network and creating a vernemq cluster

## Overview

This repo is currently in the development.
I am writing some tutorials for different parts of the pi-adhoc-mqtt-cluster.

## Used hardware and software

* Raspberry Pi 3 B+
    * batman mesh node (adhoc network wlan0)
    * bridge with lan cable eth0 for internet sharing
    * mqtt broker cluster node with vernemq
    * grafana/prometheus/influxdb for monitoring mqtt cluster and network
* several Raspberry Pi Zero W (batman mesh node)
    * batman mesh node (adhoc network wlan0)
    * mqtt broker cluster node with vernemq
    
* OS: Raspbian Stretch Lite (2018-04-18-raspbian-stretch-lite.img)
