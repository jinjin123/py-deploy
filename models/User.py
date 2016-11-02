#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
from . Base import BaseModel
from mapping import FabricSession
from mapping.User import UserMapping

from . import Singleton

class UserModel( BaseModel ):
    __metaclass__ = Singleton

    def verifyUser(self, username, password ):
        """ verify user with password """
        res = {}
        fabric = FabricSession()
        try :
            password = self._convertPassword(password)
            user = fabric.query(UserMapping).filter(UserMapping.loginname == username).first()
        except Exception as e :
            pass
        finally :
            fabric.close()

        if user is None :
            res['status'] = 'error'
            res['msg'] = 'not_register'
        else :
            if password != user.password :
                res['status'] = 'error'
                res['msg'] = 'password_error'
            else :
                res['status'] = 'success'
                res['username'] = user.nickname
                res['msg'] = 'login_success'

        return res

    def _convertPassword(self, writing):
        md5 = hashlib.md5()
        md5.update( writing.encode() )
        return md5.hexdigest()
