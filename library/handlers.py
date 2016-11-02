#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from tornado.web import RequestHandler
from library.utils import Utils

class BaseHandler( RequestHandler ) :
    def __init__(self , application , request , **kwargs ):
        super( BaseHandler , self ).__init__( application , request , **kwargs )

    def compute_etag(self):
        """ 取消缓存 """
        return None

    def prepare( self ):
        pass

    def get_current_user(self):
        return self.get_cookie('is_login')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.write("404")
        elif status_code == 500:
            self.write("500")
        else:
            self.write(str(status_code))

        self.finish()

    def set_custom_cookie(self, name, value):
        self.set_secure_cookie(name, value, expires=Utils.cookieExpire())

    def on_finish(self):
        self.set_custom_cookie('_xsrf', self.xsrf_token)

    def ajax(self , result):
        """ for ajax """
        self.write( json.dumps( result ) )
        self.finish()