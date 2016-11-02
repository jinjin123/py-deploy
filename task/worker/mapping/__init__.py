#!/usr/bin/env python
# -*- coding:utf-8 -*-

from conf import conf
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import MetaData

metadata = MetaData()


fabric_engine = create_engine(conf.mysql.fabric, echo=conf.debug, pool_size=10, pool_recycle=3600)
FabricSession = sessionmaker(bind=fabric_engine)




