#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import json
from conf import conf

class BaseModel( object ):

    @staticmethod
    def rabbitmqFactory(exchange='fabric', routing_key='', message=None):
        try :
            connection = pika.BlockingConnection(pika.URLParameters(conf.rabbitmq.dsn))
            channel = connection.channel()
            channel.exchange_declare( exchange=exchange,type='direct', durable=True)
            channel.basic_publish(
                    exchange = exchange ,
                    routing_key = routing_key ,
                    body = json.dumps(message) ,
                    properties = pika.BasicProperties(
                        delivery_mode=2, # make message persistent
                    )
            )
        except Exception as e:
            pass
        finally:
            connection.close()
