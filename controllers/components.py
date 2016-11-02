#!/usr/bin/env python
# -*- coding:utf-8 -*-

from library.handlers import BaseHandler
from library.route import route

@route(r'/components/view/(.+)')
class DashboardviewHandler( BaseHandler ):
    def get(self, view , *args, **kwargs):
        self.render('components/' + view + '.html')
