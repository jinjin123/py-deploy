#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from tornado.web import authenticated
from library.handlers import BaseHandler
from library.route import route
from library.utils import Utils

from models.User import UserModel

@route(r'/login')
class LoginHandler( BaseHandler ) :
    def get(self, *args, **kwargs):
        if not self.current_user:
            self.render("login/login.html")
        else :
            self.redirect('/')

    def post(self, *args, **kwargs):
        """ login this system """
        username = self.get_argument('username', default=None)
        password = self.get_argument('password', default=None)

        res = UserModel().verifyUser( username , password )
        if res and res['status'] == 'success' :
            self.set_custom_cookie('username', res['username'])
            self.set_custom_cookie('is_login', 'yes')

        self.ajax( res )

@route(r'/logout')
class LogoutHandler( BaseHandler ):
    @authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie('is_login')
        self.clear_all_cookies()
        self.redirect( '/login' )
