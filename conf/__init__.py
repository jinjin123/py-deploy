from oslo_config import cfg
from os.path import join , dirname

conf = cfg.CONF

# common
default_opts = [
    cfg.BoolOpt('debug' , default=False, help="是否进入调试模式") ,
    cfg.IntOpt('port' , default=8888, help="设置端口号") ,
    cfg.IntOpt('expire' , default=5000000, help="COOKIE有效期") ,
]
conf.register_cli_opts( default_opts )

# mysql
mysql = cfg.OptGroup( name='mysql' , title="MySQL options" )
conf.register_group(mysql)
conf.register_cli_opts( [
    cfg.StrOpt('fabric' , default='localhost', help="MySQL DSN"),
] , mysql )

# rabbitmq
rabbitmq = cfg.OptGroup( name='rabbitmq' , title="rabbitmq options" )
conf.register_group(rabbitmq)
conf.register_cli_opts( [
    cfg.StrOpt('dsn' , default='', help="rabbitmq DSN"),
] , rabbitmq )


conf( default_config_files = [ join( dirname(__file__) , 'application.ini' ) ] )
