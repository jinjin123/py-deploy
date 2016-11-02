#!/usr/bin/env python
# -*- coding:utf-8 -*-

import uuid
import time
from . Base import BaseModel
from mapping import FabricSession
from mapping import fabric_engine
from mapping.Machine import MachineMapping, MachineTB
from mapping.FabricRelation import FabricRelationTB
from mapping.MachineRelation import MachineRelationTB
from sqlalchemy import desc
from sqlalchemy.sql import select

from . import Singleton

class MachineModel( BaseModel ):
    __metaclass__ = Singleton

    def addMachine(self, **kwargs):
        name = kwargs.get('name', None)
        desc = kwargs.get('desc', None)
        account = kwargs.get('account', None)
        password = kwargs.get('password', None)
        ip = kwargs.get('ip', None)
        auth_type = kwargs.get('auth_type', 'password')
        res = {}
        if not name :
            res['status'] = 'error'
            res['msg'] = 'not_name'
            return res
        if not desc:
            res['status'] = 'error'
            res['msg'] = 'not_desc'
            return res
        if not account:
            res['status'] = 'error'
            res['msg'] = 'not_account'
            return res
        if not password:
            res['status'] = 'error'
            res['msg'] = 'not_password'
            return res
        if not ip:
            res['status'] = 'error'
            res['msg'] = 'not_ip'
            return res
        if not auth_type:
            res['status'] = 'error'
            res['msg'] = 'no_auth_type'

        fabric = FabricSession()
        try:
            machine = MachineMapping()
            machine.id = str( uuid.uuid1() )
            machine.name = name
            machine.desc = desc
            machine.auth_type = auth_type
            machine.ip = ip
            if auth_type == 'password':
                machine.account = account
                machine.password = password
            if auth_type == 'key':
                machine.account = None
                machine.password = None
            machine.create_time = int( time.time() )
            fabric.add(machine)
            fabric.commit()
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e :
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            fabric.close()

        return res

    def getMachines(self, *args, **kwargs):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try :
            stm = select([MachineTB]).where(MachineTB.c.is_valid == 'yes').order_by(desc(MachineTB.c.create_time))
            proxy = conn.execute( stm )
            machines = proxy.fetchall() if proxy.rowcount > 0 else []
            res['data'] = [dict(x) for x in machines]
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e :
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def delMachines(self, machine=None):
        """ delete machine"""
        res = {}
        res['status'] = 'error'

        # step.1 被删除的机器不能存在待发布状态
        if MachineModel().haveNotDeployMachine(machine_id=machine, status='not_deploy'):
            res['msg'] = 'in_not_deploy_status'
            return res
        # step.2
        if MachineModel().machineIsInProject(machine_id=machine):
            res['msg'] = 'in_project_relation'
            return res

        if machine:
            conn = fabric_engine.connect()
            try:
                stmt = MachineTB.update().values(is_valid = 'no').where( MachineTB.c.id == machine )
                conn.execute(stmt)
                res['status'] = 'success'
                res['msg'] = 'ok'
            except Exception as e :
                res['status'] = 'exception'
                res['msg'] = str(e)
            finally:
                conn.close()
        else :
            res['status'] = 'error'
            res['msg'] = 'not_machines'

        return res

    def getMachineByProject(self, project_id):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            stmt = select([MachineTB]).order_by(desc(MachineRelationTB.c.create_time)).where(
                MachineTB.c.id == MachineRelationTB.c.machine_id
                ).where(
                MachineRelationTB.c.project_id == project_id
                )
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

    def haveNotDeployMachine(self, machine_id, status = 'not_deploy'):
        res = False
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricRelationTB.c.id]).where( FabricRelationTB.c.machine_id == machine_id ).where( FabricRelationTB.c.status == status ).limit(1)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0 :
                res = True
        except Exception as e:
            res = False
        finally:
            conn.close()

        return res

    def machineIsInProject(self, machine_id):
        res = False
        conn = fabric_engine.connect()
        try:
            stmt = select([MachineRelationTB.c.id]).where(MachineRelationTB.c.machine_id == machine_id).limit(1)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0:
                res = True
        except Exception as e:
            res = False
        finally:
            conn.close()

        return res

    def isInProjectByMachine(self, project_id, machine_id):
        conn = fabric_engine.connect()
        try:
            stmt = select([MachineRelationTB.c.id]).where( MachineRelationTB.c.project_id == project_id ) \
            .where( MachineRelationTB.c.machine_id == machine_id )
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0:
                res = True
            else :
                res = False
        except Exception as e:
            res = False
        finally:
            conn.close()

        return res

    def isInFabricByMachine(self, fabric_id, machine_id):
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricRelationTB.c.id]).where(FabricRelationTB.c.fabric_id == fabric_id) \
                .where(FabricRelationTB.c.machine_id == machine_id)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0:
                res = True
            else:
                res = False
        except Exception as e:
            res = False
        finally:
            conn.close()

        return res

    def getMachineInfo(self, machine_id):
        res = {}
        res['status'] = 'error'
        conn = fabric_engine.connect()
        try:
            res['status'] = 'success'
            res['msg'] = 'ok'
            stmt = select( [MachineTB] ).where( MachineTB.c.id == machine_id ).limit(1)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0 :
                res['data'] = dict(proxy.fetchone())
            else:
                res['data'] = None
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res

    def editMachine(self, id, name, account, password, desc, ip, auth_type):
        res = {}
        res['status'] = 'error'
        if auth_type == 'password':
            if not account :
                res['msg'] = 'outof_account'
                return res
            if not password :
                res['msg'] = 'outof_password'
                return res
        if auth_type == 'key':
            password = None

        conn = fabric_engine.connect()
        try:
            upstmt = MachineTB.update().values(
                name = name,
                account = account,
                password = password,
                desc = desc,
                ip = ip,
                auth_type=auth_type
            ).where( MachineTB.c.id == id )
            conn.execute(upstmt)
            res['status'] = 'success'
            res['msg'] = 'ok'
        except Exception as e:
            res['status'] = 'exception'
            res['msg'] = str(e)
        finally:
            conn.close()

        return res


