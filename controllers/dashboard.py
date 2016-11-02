#!/usr/bin/env python
# -*- coding:utf-8 -*-

from library.handlers import BaseHandler
from library.route import route

@route(r'/dashboard/view/(.+)')
class DashboardviewHandler( BaseHandler ):
    def get(self, view , *args, **kwargs):
        self.render('dashboard/' + view + '.html')

@route(r'/dashboard')
class DashboardHandler( BaseHandler ):
    def get(self, *args, **kwargs):
        self.write('dashboard/index.html')