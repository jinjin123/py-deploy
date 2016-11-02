#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import metadata
from sqlalchemy import Column, String, Text, Integer, Table
from sqlalchemy.orm import Mapper

MachineTB = Table( 'fb_machine', metadata ,
                   Column('id', String(40), primary_key=True),
                   Column('name', String, nullable=False),
                   Column('account', String, nullable=False),
                   Column('password', String, nullable=False),
                   Column('desc', Text, nullable=True),
                   Column('create_time', Integer),
                   Column('ip', String, nullable=False),
                   Column('auth_type', String, nullable=False, default='password'),
                   Column('is_valid', String, nullable=False, default='yes'),
                )

class MachineMapping( object ):
    pass

Mapper(MachineMapping, MachineTB )



