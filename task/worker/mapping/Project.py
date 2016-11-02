#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import metadata
from sqlalchemy import Column, String, Text, Integer, Table
from sqlalchemy.orm import mapper

ProjectTB = Table('fb_project', metadata,
                  Column('id', String(40), primary_key=True),
                  Column('name', String, nullable=False),
                  Column('gituser', String, nullable=False),
                  Column('gitaddress', String, nullable=False),
                  Column('localaddress', String, nullable=False),
                  Column('remoteaddress', String, nullable=False),
                  Column('deployaddress', String, nullable=False),
                  Column('desc', Text, nullable=True),
                  Column('error', String, nullable=True),
                  Column('status', String, nullable=False, default='waiting_clone'),
                  Column('create_time', Integer),
                )

class ProjectMapping( object ):
    pass


mapper(ProjectMapping, ProjectTB)


