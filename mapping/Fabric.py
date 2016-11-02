#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import metadata
from sqlalchemy import Column , Integer , String , Table
from sqlalchemy.orm import Mapper

FabricTB = Table('fb_fabric', metadata,
               Column('id', String(40), primary_key=True),
               Column('tag', String, nullable=False),
               Column('project_id', String, nullable=False),
               Column('desc', String, nullable=True),
               Column('status', String, nullable=False, default='edit'),
               Column('type', String, nullable=False),
               Column('create_time', Integer, nullable=False),
               Column('fabric_time', Integer, nullable=True),
               Column('finish_time', Integer, nullable=True),
               Column('total', Integer, nullable=True, default=0),
               Column('success_num', Integer, nullable=True, default=0),
               Column('error_num', Integer, nullable=True, default=0),
               Column('error', String, nullable=True),
               )

class FabricMapping( object ):
    pass

Mapper( FabricMapping, FabricTB )




