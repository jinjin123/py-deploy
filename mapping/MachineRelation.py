#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import metadata
from sqlalchemy import Column, String, Text, Integer, Table
from sqlalchemy.orm import mapper

MachineRelationTB = Table('fb_machine_relation', metadata,
                  Column('id', String(40), primary_key=True),
                  Column('project_id', String, nullable=False),
                  Column('machine_id', String, nullable=False),
                  Column('create_time', Integer),
                )

class MachineRelationMapping( object ):
    pass


mapper(MachineRelationMapping, MachineRelationTB)


