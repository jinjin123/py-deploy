#!/usr/bin/env python
# -*- coding:utf-8 -*-

import uuid
import time
from . Base import BaseModel
from mapping import FabricSession
from mapping import fabric_engine
from sqlalchemy.sql import select, bindparam
from sqlalchemy import desc, asc

from models.Machine import MachineModel

from mapping.Fabric import FabricTB, FabricMapping
from mapping.FabricRelation import FabricRelationTB
from mapping.Project import ProjectTB
from mapping.Machine import MachineTB
from mapping.MachineRelation import MachineRelationTB

from . import Singleton

class FabricModel( BaseModel ):
    __metaclass__ = Singleton

    def getFabricInfo(self, fabric_id):
        res = {}
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricTB]).where( FabricTB.c.id == fabric_id ).limit(1)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0:
                res = dict(proxy.fetchone())
            else:
                res = {}

        except Exception as e:
            res = {}
        finally:
            conn.close()

        return res

    def getTagByProject(self, project_id=None):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricTB.c.tag]).where(FabricTB.c.type == 'new').where( FabricTB.c.status =='end' ) \
            .where( FabricTB.c.total == FabricTB.c.success_num ) \
            .order_by(desc(FabricTB.c.create_time)).limit(10)
            if project_id:
                stmt = stmt.where( FabricTB.c.project_id == project_id )
            proxy = conn.execute(stmt).fetchall()
            res['data'] = [ dict(x) for x in proxy ]
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def tagExists(self, project_id, tag, fabric_id=None):
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricTB.c.tag]).where(FabricTB.c.project_id == project_id).where( FabricTB.c.type == 'new' ).where(FabricTB.c.tag == tag)
            if fabric_id:
                stmt = stmt.where( ~FabricTB.c.id == fabric_id )
            stmt = stmt.limit(1)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0 :
                res = True
            else :
                res = False
        except Exception as e:
            res = False
        finally:
            conn.close()

        return res

    def addFabric(self, *args, **kwargs):
        res = {}
        res['status'] = 'error'
        type = kwargs.get('type', None)
        project = kwargs.get('project', None)
        desc = kwargs.get('desc', None)
        tag = kwargs.get('tag', None)
        machine = kwargs.get('machine',[])
        if not type:
            res['msg'] = 'not_type'
            return res
        if not project:
            res['msg'] = 'not_project'
            return res
        if not desc:
            res['msg'] = 'not_desc'
            return res
        if not tag:
            res['msg'] = 'not_tag'
            return res

        if type == 'new' and self.tagExists(project, tag):
            res['msg'] = 'tag_already_exists'
            return res

        if type == 'tag' and not self.tagExists(project, tag):
            res['msg'] = 'tag_not_exists'
            return res

        conn = fabric_engine.connect()
        trans = conn.begin()
        try:
            fabric_id = str( uuid.uuid1() )
            stmt = FabricTB.insert().values(
                id = fabric_id,
                tag = tag,
                project_id = project,
                desc = desc,
                type = type,
                status = 'edit',
                create_time = int(time.time()),
                total = len(machine),
            )
            proxy = conn.execute(stmt)
            if int(proxy.rowcount) > 0 :
                if machine:
                    data = []
                    for x in machine:
                        tmp = {}
                        tmp['_id'] = str( uuid.uuid1() )
                        tmp['_fabric_id'] = fabric_id
                        tmp['_project_id'] = project
                        tmp['_machine_id'] = x
                        tmp['_status'] = 'not_deploy'
                        tmp['_create_time'] = int( time.time() )
                        data.append( tmp )
                    machine_stmt = FabricRelationTB.insert().values(
                        id=bindparam('_id'),
                        fabric_id=bindparam('_fabric_id'),
                        project_id=bindparam('_project_id'),
                        machine_id=bindparam('_machine_id'),
                        status = bindparam('_status'),
                        create_time = bindparam('_create_time')
                    )
                    conn.execute(machine_stmt, data)

            trans.commit()
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e :
            trans.rollback()
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def editFabric(self, id, type, project, desc, tag):
        res = {}
        res['status'] = 'error'
        if not id:
            res['msg'] = 'not_id'
            return res
        if type not in ['new','tag'] :
            res['msg'] = 'type_error'
            return res
        if not project:
            res['msg'] = 'not_project'
            return res
        if not tag:
            res['msg'] = 'not_tag'
            return res

        if type == 'new' and self.tagExists(project, tag, id):
            res['msg'] = 'tag_already_exists'
            return res

        if type == 'tag' and not self.tagExists(project, tag):
            res['msg'] = 'tag_not_exists'
            return res

        conn = fabric_engine.connect()
        try:
            upstmt = FabricTB.update().values(
                type = type,
                project_id = project,
                desc = desc,
                tag = tag,
            ).where( FabricTB.c.id == id )
            proxy = conn.execute(upstmt)
            res['status'] = 'success'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def getFabrics(self, status=None):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricTB, ProjectTB.c.name.label('project_name')]).order_by(desc(FabricTB.c.create_time)).where( FabricTB.c.project_id == ProjectTB.c.id )
            if status:
                stmt = stmt.where( FabricTB.c.status == status )

            stmt = stmt.limit(10)
            proxy = conn.execute(stmt).fetchall()
            res['data']= [dict(x) for x in proxy]
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def _getMachineByFabric(self, fabric_id):
        conn = fabric_engine.connect()
        try:
            print("验证是否有需要发布的机器存在")
            stmt = select( [FabricRelationTB.c.id] ).where( FabricRelationTB.c.fabric_id == fabric_id ).limit(1)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0 :
                res = True
            else :
                res = False
        except Exception as e:
            res = False
        finally:
            conn.close()

        return res

    def setFabricToReady(self, fabric_id):
        res = {}
        res['status'] = 'error'
        session = FabricSession()
        try:
            fabric = self._getFabricInfo(session, fabric_id)
            if self._getMachineByFabric(fabric_id):
                if fabric.status == 'edit':
                    fabric.status = 'ready'
                    session.add(fabric)
                    session.commit()
                    res['status'] = 'success'
                    res['msg'] = 'ok'
                else :
                    res['status'] = 'error'
                    res['msg'] = 'status_error'
            else :
                res['status'] = 'error'
                res['msg'] = 'no_machines'

        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            session.close()

        return res

    def _getFabricInfo(self, session, fabric_id):
        try:
            fabric = session.query(FabricMapping).filter(FabricMapping.id == fabric_id).one()
        except Exception as e:
            fabric = None
        finally:
            pass

        return fabric


    def setFabricToCalcel(self, fabric_id):
        res = {}
        res['status'] = 'error'
        session = FabricSession()
        try:
            fabric = self._getFabricInfo(session, fabric_id)
            if fabric:
                fabric.status = 'cancel'
                self.setFabricRelationStatus(fabric_id)
                session.add(fabric)
                session.commit()
                res['status'] = 'success'
                res['msg'] = 'ok'
            else:
                res['status'] = 'error'
                res['msg'] = 'not_fabric'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            session.close()

        return res

    def setFabricRelationStatus(self, fabric_id):
        conn = fabric_engine.connect()
        try:
            stmt = FabricRelationTB.update().values(status = 'cancel').where( FabricRelationTB.c.fabric_id == fabric_id )
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0 :
                res = True
            else :
                res = False
        except Exception as e:
            res = True
        finally:
            conn.close()
        return res

    def deployProject(self, fabric_id):
        res = {}
        res['status'] = 'error'
        session = FabricSession()
        try:
            fabric = self._getFabricInfo(session, fabric_id)
            if fabric and fabric.status == 'ready':
                fabric.status = 'deploying'
                session.add(fabric)
                session.commit()
                # send message to rabbitmq
                self._sendDeployMessage(fabric_id)
                res['status'] = 'success'
                res['msg'] = 'ok'
            else :
                res['status'] = 'error'
                res['msg'] = 'not_fabric'

        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            session.close()

        return res

    def _sendDeployMessage(self, fabric_id):
        # send to rabbitmq
        self.rabbitmqFactory(routing_key='deploy_project', message={'fabric_id': fabric_id} )

    def getFabricRelationMachines(self, fabric_id):
        res = {}
        res['status'] = 'success'
        conn = fabric_engine.connect()
        try:
            res['status'] = 'success'
            res['msg'] = 'ok'
            res['data'] = {}
            have_stmt = select([MachineTB]).where(FabricRelationTB.c.fabric_id == fabric_id) \
            .where( FabricRelationTB.c.machine_id == MachineTB.c.id )
            proxy = conn.execute(have_stmt).fetchall()
            res['data']['have'] = [dict(x) for x in proxy]

            fabric_info = self.getFabricInfo(fabric_id)
            res['data']['fabric_info'] = fabric_info

            not_have = select( [MachineTB] ).where( MachineRelationTB.c.machine_id == MachineTB.c.id ) \
                .where( MachineRelationTB.c.project_id == fabric_info['project_id'] ) \
                .where( ~MachineRelationTB.c.machine_id.in_(
                    select([FabricRelationTB.c.machine_id]).where( FabricRelationTB.c.fabric_id == fabric_id )
            ) )
            proxy = conn.execute( not_have ).fetchall()
            res['data']['not_have'] = [dict(x) for x in proxy]

        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def addMachineToFabric(self, fabric_id, machine_id):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            fabric_info = self.getFabricInfo(fabric_id)
            if MachineModel().isInProjectByMachine(fabric_info['project_id'], machine_id):
                if not MachineModel().isInFabricByMachine(fabric_id, machine_id):
                    inst = FabricRelationTB.insert().values(
                        id = str(uuid.uuid1()) ,
                        fabric_id = fabric_id ,
                        project_id = fabric_info['project_id'],
                        machine_id = machine_id ,
                        status = 'not_deploy' ,
                        create_time = int(time.time())
                    )
                    conn.execute(inst)
                    # update total num
                    upstmt = FabricTB.update().values( total = fabric_info['total'] + 1 ).where( FabricTB.c.id == fabric_id )
                    conn.execute(upstmt)
                    res['status'] = 'success'
                    res['msg'] = 'ok'
                else:
                    res['status'] = 'error'
                    res['msg'] = 'already_in_fabric'
            else :
                res['status'] = 'error'
                res['msg'] = 'not_in_project'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def delMachineToFabric(self, fabric_id, machine_id):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            fabric_info = self.getFabricInfo(fabric_id)
            dele = FabricRelationTB.delete().where( FabricRelationTB.c.fabric_id == fabric_id ).where( FabricRelationTB.c.machine_id == machine_id )
            conn.execute(dele)

            upstmt = FabricTB.update().values(total = fabric_info['total'] - 1).where( FabricTB.c.id == fabric_id )
            conn.execute(upstmt)

            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def allMachinesByFabric(self, fabric_id):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricRelationTB, MachineTB.c.name]).order_by(asc(FabricRelationTB.c.create_time)).where(FabricRelationTB.c.machine_id == MachineTB.c.id).where(FabricRelationTB.c.fabric_id == fabric_id)
            proxy = conn.execute(stmt).fetchall()
            res['status'] = 'success'
            res['msg'] = 'ok'
            res['data'] = [dict(x) for x in proxy ]

        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = 'ok'
        finally:
            conn.close()

        return res

    def getFabricInfoById(self, fabric_id):
        data = self.getFabricInfo(fabric_id)

        res = {}
        res['status'] = 'success'
        res['data'] = data

        return res

    @staticmethod
    def getUsableTag():
        res = {}
        res['data'] = {}
        res['status'] = 'success'
        res['msg'] = 'ok'
        res['data']['tag'] = time.strftime( "%Y-%m-%d-%H-%M-%S" , time.localtime() )
        return res



