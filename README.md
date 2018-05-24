# pi-adhoc-mqtt-cluster
Using batman-adv to connect several raspberrypi to a mesh network and creating a vernemq cluster

## Overview

This repo is currently in the development.  
It already explains how to create the batman mesh network and install vernemq on a raspberrypi.  
Currently I am adding some tutorials for different parts of the pi-adhoc-mqtt-cluster.  
Feel free to comment.

## Used hardware and software

* Raspberry Pi 3 B+
    * batman mesh node (adhoc network wlan0)
    * bridge with lan cable eth0 for combining mesh and different network
    * internet gateway with dhcp server for sharing eth0 internet with mesh nodes
    * mqtt broker cluster node with vernemq
    * grafana/prometheus/influxdb for monitoring mqtt cluster and network (not written yet)
* several Raspberry Pi Zero W (batman mesh node)
    * batman mesh node (adhoc network wlan0)
    * mqtt broker cluster node with vernemq
    
* OS: Raspbian Stretch Lite (2018-04-18-raspbian-stretch-lite.img)

## Links to the tutorials:

Links to different parts:

* [Batman-adv and Batctl](https://github.com/suiluj/pi-adhoc-mqtt-cluster/wiki/Batman-Adv-and-Batctl)
* [VerneMQ](https://github.com/suiluj/pi-adhoc-mqtt-cluster/wiki/VerneMQ)
