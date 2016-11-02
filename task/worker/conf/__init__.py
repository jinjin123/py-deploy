#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oslo_config import cfg
from os.path import join , dirname

conf = cfg.CONF

# common
default_opts = [
    cfg.BoolOpt(name='debug', default=False),
    cfg.StrOpt(name='savepath', default='/tmp'),
    cfg.StrOpt(name='secretkey', default='/root/.ssh/id_rsa'),
    cfg.StrOpt(name='username', default='fabric'),
    cfg.StrOpt(name='email', default='fabric@xuebanapp.com'),
    cfg.StrOpt(name='ossprefix', default='xueban'),
]
conf.register_cli_opts( default_opts )

# clone
clone = cfg.OptGroup( name='clone' , title="clone project config" )
conf.register_group(clone)
conf.register_opts( [
    cfg.StrOpt('queue' , default=''),
    cfg.StrOpt('exchange' , default=''),
] , clone )

# deploy
deploy = cfg.OptGroup( name='deploy' , title="deploy config" )
conf.register_group(deploy)
conf.register_cli_opts( [
    cfg.StrOpt('queue' , default=''),
    cfg.StrOpt('exchange' , default=''),
] , deploy )


# rabbitmq
rabbitmq = cfg.OptGroup( name='rabbitmq' , title="rabbitmq config" )
conf.register_group(rabbitmq)
conf.register_cli_opts( [
    cfg.StrOpt('dsn' , default=''),
] , rabbitmq )

# mysql
mysql = cfg.OptGroup( name='mysql' , title="mysql config" )
conf.register_group(mysql)
conf.register_cli_opts( [
    cfg.StrOpt('fabric' , default='localhost'),
] , mysql )

# auth
auth = cfg.OptGroup( name='auth' , title="auth config" )
conf.register_group(auth)
conf.register_cli_opts( [
    cfg.StrOpt('pubkey' , default=''),
    cfg.StrOpt('privkey' , default=''),
    cfg.StrOpt('username' , default=''),
] , auth )

# oss
oss = cfg.OptGroup( name='oss', title="aliyun's oss")
conf.register_group(oss)
conf.register_cli_opts([
    cfg.StrOpt('endpoint',default='http://oss-cn-hangzhou-internal.aliyuncs.com'),
    cfg.StrOpt('accessid',default='I0E1ZSS1bl40tjNr'),
    cfg.StrOpt('accesssecret',default='FDOrbRd4UoXfuETnXl6vYZT2xeGnSI'),
    cfg.StrOpt('bucket',default='bingo-workstation'),
],oss )


conf( default_config_files = [ join( dirname(__file__) , 'conf.ini' ) ] )
