该系统主要用于PHP代码的发布和回滚，主要业务对象为项目和机器。项目关联服务器，针对项目进行版本发布，针对Git仓库的TAG进行回滚，目前仅支持全量发布和回滚，
不支持单文件的发布。

该系统可部署在单独的服务器上，但消息worker端必须与Git仓库部署在一起

使用的python扩展如下：

  angularjs

  tornado

  oslo.config

  sqlalchemy

  python-mysql

  fabric3

  pika

  pygit2

  oss2

以下为项目截图：

首页：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E9%A6%96%E9%A1%B5.gif)

机器列表：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E6%9C%BA%E5%99%A8%E5%88%97%E8%A1%A8.gif)

添加机器：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E6%B7%BB%E5%8A%A0%E6%9C%BA%E5%99%A8.gif)

项目列表：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E9%A1%B9%E7%9B%AE%E5%88%97%E8%A1%A8.gif)

添加项目：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E6%B7%BB%E5%8A%A0%E9%A1%B9%E7%9B%AE.gif)

发布历史：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E5%8F%91%E5%B8%83%E5%8E%86%E5%8F%B2.gif)

全新发布：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E5%85%A8%E6%96%B0%E5%8F%91%E5%B8%83.gif)

回滚发布：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E5%9B%9E%E6%BB%9A%E5%8F%91%E5%B8%83.gif)

发布详情：
![image](https://github.com/xiaowan/py-deploy/blob/master/snapshot/%E5%8F%91%E5%B8%83%E8%AF%A6%E6%83%85.gif)
