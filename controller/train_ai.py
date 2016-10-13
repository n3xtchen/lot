#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 n3xtchen <echenwen@gmail.com>
#
# Distributed under terms of the GPL-2.0 license.

"""

"""

import random, time

WAIT_SERVO_TIME = 1

trains = {
    "t1": "4",
    "t2": "5",
    "t3": "6",
}

nodes = {
    "735967": "A",
    "844963": "B",
    "826777": "C",
    "573026": "D",
    "14597272": "E",
    "843949": "F",
    "14488991": "G",
    "14572685": "H",
    "14572687": "I",
    "14449326": "J",
    "14577221": "K",
    "707087": "L",
    "14449257": "M",
    "14597177": "N",
    "844877": "O",
    "796683": "P",
    "14572657": "Q",
    "589046": "R",
    "216605": "S",
    "14449038": "T",
    "14485279": "U",
    "14489405": "V",
    "14485153": "W",
    "14597306": "X",
    "14597212": "Y",
    "14449320": "Z"
}

paths = {
    "A": {"B": False},
    "B": {"C": ["6:1350"], "W": ["6:1900"]},
    "C": {"D": False},
    "D": {"E": False},
    "E": {"F": ["1:1600"], "K": ["1:1050"]},
    "F": {"G": False},
    "G": {"H": False},
    "H": {"I": False},
    "I": {"J": False},
    "J": {"A": False},
    "K": {"L": ["3:1700"]},
    "L": {"M": ["4:1700"]},
    "M": {"N": ["5:1250"], "R": ["5:1850"]},
    "N": {"O": False},
    "O": {"P": False},
    "P": {"Q": False},
    "Q": {"H": False},
    "R": {"S": ["7:1750"]},
    "S": {"T": False},
    "T": {"U": False},
    "U": {"V": False},
    "V": {"L": ["2:1600", "3:1200"]},
    "W": {"E": False},
    "X": {"L": ["2:1100", "3:1200"]},
    "Y": {"M": ["4:1000"]},
    "Z": {"S": ["7:1150"]}
}

# 高速路段
high_speed_path = [
    # [source, target]
]

TRAIN_STOP = 0
TRAIN_RUN = 1
TRAIN_BACK = 2
TRAIN_HIGH = 3

class Train(object):

    def __init__(self, id, start_node, sender):
        self.id = id    # 火车标识
        self.at = start_node # 所在的节点，就是最后RFID
        self.occupied = []  # 占用的节点
        self.sender = sender # 信息发射端
        self.status = TRAIN_STOP # 火车状态, 0: 停止，1: 运行, -1: 倒退
        self.speed = 1 # 速度, 1: 正常, 2: 加速

    def find_a_way_out_from(self, n, trains):
        path = paths[n]
        x =  [x.occupied for x in trains.values()]
        occupied = set(reduce(lambda x, y: x+y, x)) - set(self.occupied)
        targets = list(set(path.keys()) - occupied)
        if len(targets) >= 1:
            r_int = random.randint(0, len(targets)-1)
            node = targets[r_int]
            return {"id": node, "servo": path[node]} 
        else:
            return False

    def next(self, trains, source=None):
        if source == None:
            source = self.at
        target = self.find_a_way_out_from(source, trains)
        print self.id, "should go", target
        if target != False:
            self.occupied = [source, target["id"]]
            if target["servo"]:
                self.status = 0
                self.sender.send('outputs', str(self.id), TRAIN_STOP)
                print target
                for servo in target["servo"]:
                    servo_id, status = servo.split(":")
                    print "扳道"
                    self.sender.send('outputs', str(servo_id), status)
                time.sleep(WAIT_SERVO_TIME)   # 等待操作完成
            self.speed = 1 if self.occupied not in high_speed_path else 2
            self.status = 1
            self.sender.send('outputs', str(self.id), TRAIN_RUN if self.speed == 1 else TRAIN_HIGH)
        else:
            self.status = 0
            self.at = source
            self.sender.send('outputs', str(self.id), TRAIN_STOP)

