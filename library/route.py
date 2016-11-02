#!/usr/bin/env pyhon
# -*- coding:utf8 -*-

class Route(object):
    def __init__(self):
        self.url_list = list()

    def __call__(self, _url , name=None):
        def _(cls):
            self.url_list.append( ( _url, cls) )

            return cls

        return _

route = Route()
