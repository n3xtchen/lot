#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 n3xtchen <echenwen@gmail.com>
#
# Distributed under terms of the GPL-2.0 license.

"""

"""

import re
import paho.mqtt.client as mqtt
from train_ai import *

REGEX_INPUT = re.compile(r"^(\w{32})/inputs/(\d+)$")

class Sender(object):
    def __init__(self, mq, uid):
        self.mqtt = mq
        self.prefix = uid
    def send(self, direct, id, status):
        self.mqtt.publish(self.prefix+"/"+direct+"/"+id, status)

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(userdata.get('uid') + '/#')

def on_message(client, userdata, msg):
    print(msg.topic+":"+msg.payload)
    m = REGEX_INPUT.match(msg.topic)
    if m and m.group(1) == userdata.get('uid'):
        id = str(m.group(2))
        dt = str(msg.payload)
        if dt != str(TRAIN_BACK):
            if id not in trains:
                train = Train(id, None, sender)
                trains[id] = train
            else:
                train =trains[id]
            if dt in nodes:
                print(id + ": " + nodes[dt])
                train.at = nodes[dt]
                train.next(trains, nodes[dt])
        else:
            print("火车{}在倒车，接触控制".format(id))
            del(trains[id])

host = "www.busykoala.com"
port = 1883
trains = {}
uid = 'c1eb0783873f4a2ba6eb1ad2a76be93d'

mqttc = mqtt.Client(userdata={"uid":uid})
sender = Sender(mqttc, uid)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(host, port)
mqttc.loop_start()

try:
    while True:
        for train in trains.values():
            if train.status == 0:
                train.next(trains)
except (KeyboardInterrupt, SystemExit):
    mqttc.loop_stop()
    mqttc.disconnect()

