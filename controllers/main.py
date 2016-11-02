#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado.web import authenticated
from library.handlers import BaseHandler
from library.route import route

@route(r'/')
class MainHandler( BaseHandler ):
    @authenticated
    def get(self, *args, **kwargs):
        self.render( 'main/index.html' ,
                     username = self.get_secure_cookie('username')
                     )
