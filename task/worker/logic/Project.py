#!/usr/bin/env python
# -*- coding:utf-8 -*-

from conf import conf
from logic.Base import BaseModel
from mapping import fabric_engine
from mapping.Project import ProjectTB
from sqlalchemy.sql import select
from ellen.repo import Jagare

from . import Singleton

class ProjectModel( BaseModel ):
    __metaclass__ = Singleton

    def getInfoByProjectId(self, project_id):
        """ get info by project id"""
        res = {}
        conn = fabric_engine.connect()
        try :
            result = conn.execute(select([ProjectTB]).where(ProjectTB.c.id == project_id))
            if result.rowcount != 0:
                res = dict( result.fetchone() )
            else :
                pass
        except Exception as e:
            pass
        finally:
            conn.close()

        return res

    def updateProjectState(self, project_id, status, error=None):
        res = False
        conn = fabric_engine.connect()
        try:
            stmt = ProjectTB.update().values( status = status, error = error ).where( ProjectTB.c.id == project_id )
            resPro = conn.execute(stmt)
            if int( resPro.rowcount ) > 0 :
                res = True
            else:
                res = False
        except Exception as e :
            pass
        finally:
            conn.close()

        return res

    @staticmethod
    def cloneRepo(payload):
        """ clone to local """
        project_id = payload.get('project_id', None)
        pro = ProjectModel()
        project_info = pro.getInfoByProjectId(project_id)
        error = None
        if project_info:
            try :
                Jagare.clone(project_info['gitaddress'], project_info['localaddress'],
                                 callbacks=Jagare.auth(project_info['gituser'], conf.auth.pubkey, conf.auth.privkey, '')
                                 )
                res_string = 'ready'
            except Exception as e:
                res_string = 'clone_error'
                error = str(e)
        else:
            res_string = 'no_project'
            error = 'not found this project'

        pro.updateProjectState(project_id, res_string, error)

        return 'success'



