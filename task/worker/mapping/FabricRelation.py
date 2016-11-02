#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import metadata
from sqlalchemy import Column , Integer , String , Table
from sqlalchemy.orm import Mapper

FabricRelationTB = Table('fb_fabric_relation', metadata,
               Column('id', String(40), primary_key=True),
               Column('fabric_id', String, nullable=False),
               Column('project_id', String, nullable=False),
               Column('machine_id', String, nullable=False),
               Column('status', String, nullable=False, default='not_deploy'),
               Column('error', String, nullable=True),
               Column('create_time', Integer, nullable=False),
               Column('fabric_time', Integer, nullable=True),
               Column('finish_time', Integer, nullable=True),
               )

class FabricRelationMapping( object ):
    pass

Mapper( FabricRelationMapping, FabricRelationTB )




