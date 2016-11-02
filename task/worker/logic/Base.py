#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
from conf import conf
import time
from os.path import join, dirname
import oss2
import logging

class BaseModel( object ):

    @staticmethod
    def rabbitmqWorkerFactory(dsn='', exchange='', queue='', callback=None ):
        # connection mq
        connection = pika.BlockingConnection(pika.URLParameters(dsn))
        channel = connection.channel()

        # declare exchange
        channel.exchange_declare(exchange=exchange, type='direct', durable=True)

        # declare queue
        result = channel.queue_declare(queue=queue, durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=exchange, queue=queue_name)

        # config for rabbitmq'worker
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue=queue, no_ack=True)

        channel.start_consuming()

    @staticmethod
    def getLogger(fabric_id, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        filepath = lambda fabric_id: join(dirname(dirname(__file__)), 'logs', fabric_id + '.log')
        fh = logging.FileHandler( filepath(fabric_id) )
        fh.setLevel( logging.DEBUG )
        fh.setFormatter( logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S') )

        logger.addHandler(fh)

        return logger

    @staticmethod
    def buildOssPath(localpath, fabric_time, tag, mode='tar.gz'):
        # osspath = ossprefix + project_name + year + month + tag.mode
        project_name = localpath.split('/')[-1]
        year = str(time.strftime('%Y', time.localtime(fabric_time)))
        month = str(time.strftime('%m', time.localtime(fabric_time)))
        return join( conf.ossprefix, project_name, year, month, tag + '.' + mode)

    @staticmethod
    def uploadFileToOss(local=None, remote=None):
        auth = oss2.Auth( conf.oss.accessid , conf.oss.accesssecret )
        bucket = oss2.Bucket( auth , conf.oss.endpoint , conf.oss.bucket )
        bucket.put_object_from_file( remote , local , headers=None)

    @staticmethod
    def buildpath( savepath, localpath, fabric_time, tag, mode='tar.gz' ):
        # path = savepath + project_name + year + month + tag.mode
        project_name = localpath.split('/')[-1]
        year = str( time.strftime('%Y', time.localtime(fabric_time) ) )
        month = str( time.strftime('%m', time.localtime(fabric_time) ) )
        return join( savepath, project_name, year, month , tag + '.' + mode )
