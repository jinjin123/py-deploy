#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import uuid
from models.Base import BaseModel
from mapping import FabricSession
from mapping import fabric_engine
from mapping.Project import ProjectMapping, ProjectTB
from mapping.Machine import MachineTB
from mapping.MachineRelation import MachineRelationTB
from sqlalchemy import desc
from sqlalchemy.sql import select, bindparam, and_

from . import Singleton

import os
from os.path import join, isfile, isdir

import pygit2


class ProjectModel( BaseModel ):
    __metaclass__ = Singleton

    def addProject(self, **kwargs):
        name = kwargs.get('name', None)
        gituser = kwargs.get('gituser', None)
        gitaddress = kwargs.get('gitaddress', None)
        localaddress = kwargs.get('localaddress', None)
        remoteaddress = kwargs.get('remoteaddress', None)
        deployaddress = kwargs.get('deployaddress', None)
        desc = kwargs.get('desc', None)
        create_time = int(time.time())
        res = {}
        if not name :
            res['status'] = 'error'
            res['msg'] = 'not_project_name'
        if not gitaddress:
            res['status'] = 'error'
            res['msg'] = 'not_gitaddress'
        if not localaddress:
            res['status'] = 'error'
            res['msg'] = 'not_localaddress'
        if not remoteaddress:
            res['status'] = 'error'
            res['msg'] = 'not_remoteaddress'
        if not deployaddress:
            res['status'] = 'error'
            res['msg'] = 'not_deployaddress'
        if not gituser:
            res['status'] = 'error'
            res['msg'] = 'not_gituser'

        fabric = FabricSession()
        try:
            project = ProjectMapping()
            project.id = str( uuid.uuid1() )
            project.name = name
            project.gituser = gituser
            project.gitaddress = gitaddress
            project.localaddress = localaddress
            project.remoteaddress = remoteaddress
            project.deployaddress = deployaddress
            project.desc = desc
            project.create_time = create_time
            fabric.add( project )
            fabric.commit()
            res['status'] = 'success'
            res['msg'] = 'ok'

            self._sendCloneMessage( project.id )

        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            fabric.close()

        return res

    def editProject(self, id, name, desc, gituser, gitaddress, localaddress, remoteaddress, deployaddress):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            upstmt = ProjectTB.update().values(
                name = name,
                gituser = gituser,
                gitaddress = gitaddress,
                localaddress = localaddress,
                remoteaddress = remoteaddress,
                deployaddress = deployaddress,
                desc = desc,
            ).where( ProjectTB.c.id == id )
            conn.execute(upstmt)
            res['status'] = 'success'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def _sendCloneMessage(self, project_id):
        # send to rabbitmq
        self.rabbitmqFactory(routing_key='clone_project',
                             message={'project_id': project_id},
                             )

    def delProjects(self, projects=None):
        res = {}
        if not projects:
            res['status'] = 'error'
            res['msg'] = 'not_projects'

        fabric = FabricSession()
        try:
            print(projects)
            fabric.query( ProjectMapping ).filter( ProjectMapping.id.in_(projects) ).delete(synchronize_session=False)
            fabric.commit()
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e :
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            fabric.close()

        return res

    def _getProjectInfo(self, project_id):
        """ get info by project id"""
        conn = fabric_engine.connect()
        result = conn.execute( select([ProjectTB]).where( ProjectTB.c.id == project_id ) )
        if result.rowcount != 0:
            res = dict( result.fetchone() )
        else :
            res = {}
        conn.close()
        return res


    def getInfoByProjectId(self, project_id):
        """ get info by project id"""
        proxy = self._getProjectInfo(project_id)
        res = {}
        res['status'] = 'success'
        res['data'] = proxy
        return res

    def tryAgain(self, project_id):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            stmt = ProjectTB.update().values(status='cloneing').where(ProjectTB.c.id == project_id)
            resPro = conn.execute(stmt)
            if int(resPro.rowcount) > 0:
                self._sendCloneMessage(project_id)

                res['status'] = 'success'
                res['msg'] = 'ok'
            else:
                res['msg'] = 'not_project'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def getRelationMachines(self, project_id=None):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            res['data'] = {}
            res['data']['have'] = []
            res['data']['not_have'] = []
            stm_have = select([MachineTB]).where(and_(
                MachineRelationTB.c.machine_id == MachineTB.c.id,
                MachineRelationTB.c.project_id == bindparam("project_id"),
            ))
            have = conn.execute(stm_have, project_id=project_id).fetchall()
            res['data']['have'] = [dict(x) for x in have]

            stm_no_have = select([MachineTB]).where(
                ~MachineTB.c.id.in_(
                    select([MachineRelationTB.c.machine_id]).where(
                        MachineRelationTB.c.project_id == bindparam("project_id")
                    )
                )
            ).where( MachineTB.c.is_valid == 'yes' )
            not_have = conn.execute(stm_no_have, project_id=project_id).fetchall()
            res['data']['not_have'] = [dict(y) for y in not_have]
            res['status'] = 'success'

        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def addRelation(self, project_id, machine_id = []):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            data = []
            for x in machine_id:
                tmp = {}
                tmp['_id'] = str( uuid.uuid1() )
                tmp['_project_id'] = project_id
                tmp['_machine_id'] = x
                tmp['_create_time'] = int( time.time() )
                data.append(tmp)

            stmt = MachineRelationTB.insert().values( id=bindparam('_id'), project_id=bindparam('_project_id'), machine_id=bindparam('_machine_id'), create_time=bindparam('_create_time')  )
            conn.execute(stmt, data)
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def delRelation(self, project, machine):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            for x in machine:
                stmt = MachineRelationTB.delete().where( MachineRelationTB.c.project_id == project ).where( MachineRelationTB.c.machine_id == x )
                conn.execute( stmt )

            res['status'] = 'success'
            res['msg'] = 'ok'

        except Exception as e :
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def getAllProject(self, status=None):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            stmt = select([ProjectTB])
            if status:
                stmt = stmt.where(ProjectTB.c.status == status)

            stmt.order_by( desc(ProjectTB.c.create_time) )

            proxy = conn.execute(stmt).fetchall()

            res['data'] = [dict(x) for x in proxy]
            res['status'] = 'success'
            res['msg'] = 'ok'

        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res





