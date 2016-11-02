from tornado.options import options , define
from conf import conf
import time


class Utils( object ) :

    @staticmethod
    def parser_config():
        """Rewrite tornado default parser_config_file.
        """
        for name in conf :
            value = conf.get(name)
            if name in options :
                options[name].set( value )
            else :
                define( name , default=value )

    @staticmethod
    def timeformat(timestamp, format='%Y-%m-%d %H:%M:%S', default='-'):
        if timestamp :
            return time.strftime(format, time.localtime(timestamp))
        else :
            return default

    @staticmethod
    def cookieExpire():
        return time.time() + conf.expire

