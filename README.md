该系统主要用于PHP代码的发布和回滚，主要业务对象为项目和机器。项目关联服务器，针对项目进行版本发布，针对Git仓库的TAG进行回滚，目前仅支持全量发布和回滚，
不支持单文件的发布。

该系统可部署在单独的服务器上，但消息worker端必须与Git仓库部署在一起

使用的python扩展如下：

  tornado

  oslo.config

  sqlalchemy

  python-mysql

  fabric3

  pika

  pygit2

  oss2
