#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import metadata
from sqlalchemy import Column , Integer , String , Table
from sqlalchemy.orm import Mapper

UserTB = Table('fb_user', metadata,
               Column('id', String(40), primary_key=True),
               Column('loginname', String(40), nullable=False),
               Column('nickname', String, nullable=False),
               Column('password', String, nullable=False),
               Column('avatar', String, nullable=True),
               Column('create_time', Integer)
               )

class UserMapping( object ):
    pass

Mapper( UserMapping, UserTB )




