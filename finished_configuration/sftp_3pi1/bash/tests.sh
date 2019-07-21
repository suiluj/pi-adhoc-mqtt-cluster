#!/bin/bash

CONFIG_FILE=/home/pi/vernemq/_build/rpi32/rel/vernemq/etc/vernemq.conf
TARGET_KEY=nodename

VERNEMQNODENAME=$(cat $CONFIG_FILE | grep $TARGET_KEY | cut -d ' ' -f 3)
echo "${VERNEMQNODENAME}"


# APINTERFACESTATUS="$(cat /sys/class/net/ap0/operstate)"
# # echo "${APINTERFACESTATUS}"
# if [ "$APINTERFACESTATUS" != "up" ]
# then
#     echo "interface ap0 was not up - now setting up..."
#     sudo ip link set ap0 up
# else
#     echo "interface ap0 was already set up"
# fi

# CONFIG_FILE=/etc/hostapd/hostapd.conf
# TARGET_KEY=channel

# CURRENTCHANNEL=$(iwlist wlan1 channel | grep "Current" | grep -o '[0-9]*'| tail -n 1)
# CONFIGCHANNEL=$(cat $CONFIG_FILE | grep "channel" | grep -o '[0-9]*'| tail -n 1)
# # echo "${CHANNELLINE}"


# if [ -n "$CURRENTCHANNEL" ]
# then
#     if [ "$CURRENTCHANNEL" != "$CONFIGCHANNEL" ]
#     then
#         echo "Changing AP channel and restarting hostapd"
#         REPLACEMENT_VALUE=$CURRENTCHANNEL

#         sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE

#         sudo systemctl restart hostapd.service
#     else
#         echo "AP and client channels are already the same"
#     fi
# else
#     echo "there is no current wifi client channel"
# fi
