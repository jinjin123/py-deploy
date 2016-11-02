#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from conf import conf
from logic.Fabric import FabricModel
from logic.Base import BaseModel

def task(ch, method, properties, body):
    body = body.decode()
    payload = json.loads(body)
    print("接收到消息,开始处理")
    FabricModel.deployFabric(payload)

if __name__ == '__main__' :
    print("开始监听队列")
    BaseModel.rabbitmqWorkerFactory( conf.rabbitmq.dsn, conf.deploy.exchange, conf.deploy.queue, task )