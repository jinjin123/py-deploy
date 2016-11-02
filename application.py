#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path
import tornado
from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options
from library.utils import Utils
from library.urls import urls
from tornado.web import StaticFileHandler
from controllers.errors import NotFoundHandler

class Application ( web.Application  ) :
    def __init__( self ) :

        settings = dict(
            debug = options.debug ,
            template_path = os.path.join( os.path.dirname(__file__) , "templates" ) ,
            xsrf_cookies = True ,
            cookie_secret = 'abc!@#$%^&*(()HJK' ,
            login_url = '/login' ,
            static_path = os.path.join( os.path.dirname(__file__) , "assets" ) ,
            autoreload = options.debug ,
            default_handler_class = NotFoundHandler
        )
        urls.append( ( r'/assets/(.*)' , StaticFileHandler , dict( path = os.path.join(os.path.dirname(__file__) , 'assets') ) ) )

        super( Application , self ).__init__(urls , **settings )


def main():
    Utils.parser_config()
    tornado.options.parse_command_line()

    http_server = HTTPServer( Application() , xheaders = True )
    http_server.listen(options.port)
    IOLoop.instance().start()

if __name__ == '__main__' :
    main()

