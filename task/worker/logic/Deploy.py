#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path
import time
from fabric import api
from conf import conf
from . import Singleton
from logic.Base import BaseModel
from logic.Exceptions import DeployException
from mapping import fabric_engine
from mapping.Machine import MachineTB
from sqlalchemy.sql import select
from mapping.FabricRelation import FabricRelationTB


class DeployModel( BaseModel ):
    __metaclass__ = Singleton

    def __init__(self, fabric, project, filepath):
        self.fabric = fabric
        self.filepath = filepath
        self.project = project

        self.remoteaddress = (self.project)['remoteaddress']  # save code
        self.deployaddress = (self.project)['deployaddress']  # deploy code
        self.filename = os.path.basename( self.filepath )     # tar.gz filename
        self.fullpath = os.path.join(self.remoteaddress, self.filename) # this full name

        # logger
        self.logger = BaseModel.getLogger((self.fabric)['id'],'deploy')

    def updateFabricRelationInfo(self, relation_id, status, error, fabric_time, finish_time):
        conn = fabric_engine.connect()
        try:
            stmt = FabricRelationTB.update().values(status=status, error=error, fabric_time=fabric_time, finish_time=finish_time )
            stmt = stmt.where( FabricRelationTB.c.id == relation_id )
            conn.execute(stmt)
        except Exception as e:
            pass
        finally:
            conn.close()

    def deployMachineByFabric(self):
        self.logger.info("开始部署代码")
        machines = self.getMachinesWaitingDeploy()
        if machines:
            self.logger.info("获取到所有需要部署代码的机器")
            # start to deploy to machine
            success = 0
            error = 0
            for item in machines:
                self.logger.info("开始发布" + str(item['ip']))
                fabric_time = int( time.time() )
                with api.settings( api.hide('stdout'), warn_only=True, host_string=item['ip'], user=item['account'], abort_on_prompts=True, abort_exception=DeployException ):
                    # set auth type for machines
                    if item['auth_type'] == 'password' :
                        self.logger.info("账号密码登陆")
                        api.env.password = item['password']
                    elif item['auth_type'] == 'key' :
                        self.logger.info("秘钥登陆")
                        api.env.key_filename = conf.secretkey

                    # step.1 cp
                    try:
                        self.logger.info("开始拷贝")
                        copy = self.copyToRemote()
                        if copy.failed:
                            self.logger.info("拷贝失败")
                            self.updateFabricRelationInfo(
                                relation_id=item['id'],
                                status='error',
                                error='拷贝失败',
                                fabric_time=fabric_time,
                                finish_time=int(time.time())
                            )
                            error += 1
                            continue
                        else:
                            self.logger.info("拷贝成功")
                    except DeployException as e:
                        self.logger.info("拷贝异常")
                        self.updateFabricRelationInfo(
                            relation_id=item['id'],
                            status='error',
                            error=str(e),
                            fabric_time=fabric_time,
                            finish_time=int(time.time())
                        )
                        error += 1
                        continue

                    # step.2 tar -zxvf
                    try:
                        self.logger.info("开始解压")
                        extrace = self.extraceCode()
                        if extrace.failed:
                            self.logger.info("解压失败")
                            self.updateFabricRelationInfo(
                                relation_id=item['id'],
                                status='error',
                                error='解压失败',
                                fabric_time=fabric_time,
                                finish_time=int(time.time())
                            )
                            error += 1
                            continue
                        else:
                            self.logger.info("解压成功")
                    except DeployException as e:
                        self.logger.info("解压异常")
                        self.updateFabricRelationInfo(
                            relation_id=item['id'],
                            status='error',
                            error=str(e),
                            fabric_time=fabric_time,
                            finish_time=int(time.time())
                        )
                        error += 1
                        continue

                    success+=1

                    # step.3 remove code file
                    try:
                        self.logger.info("删除压缩包")
                        remove = self.removeCode()
                        if remove.failed:
                            self.logger.info("删除失败")
                            self.updateFabricRelationInfo(
                                relation_id=item['id'],
                                status='warning',
                                error=remove.stdout,
                                fabric_time=fabric_time,
                                finish_time=int(time.time())
                            )
                        else:
                            self.logger.info("删除成功")
                            self.updateFabricRelationInfo(
                                relation_id=item['id'],
                                status='success',
                                error=None,
                                fabric_time=fabric_time,
                                finish_time=int(time.time())
                            )

                    except DeployException as e:
                        self.logger.info("删除异常")
                        self.updateFabricRelationInfo(
                            relation_id=item['id'],
                            status='warning',
                            error=str(e),
                            fabric_time=fabric_time,
                            finish_time=int(time.time())
                        )

                    # step.4 power control
                    try:
                        self.logger.info("修改代码文件权限")
                        power = self.powerControl()
                        if power.failed:
                            self.logger.info("代码文件权限修改失败")
                            self.updateFabricRelationInfo(
                                relation_id=item['id'],
                                status='warning',
                                error=power.stdout,
                                fabric_time=fabric_time,
                                finish_time=int(time.time())
                            )
                        else:
                            self.logger.info("代码文件权限修改成功")
                            self.updateFabricRelationInfo(
                                relation_id=item['id'],
                                status='success',
                                error=None,
                                fabric_time=fabric_time,
                                finish_time=int(time.time())
                            )

                    except DeployException as e:
                        self.logger.info("代码文件权限修改异常")
                        self.updateFabricRelationInfo(
                            relation_id=item['id'],
                            status='warning',
                            error=str(e),
                            fabric_time=fabric_time,
                            finish_time=int(time.time())
                        )

            self.logger.info("所有机器部署完毕")
            return {
                'success': success,
                'error': error
            }


    def getMachinesWaitingDeploy(self):
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricRelationTB.c.id, MachineTB.c.ip, MachineTB.c.account, MachineTB.c.password, MachineTB.c.auth_type]).where( MachineTB.c.id == FabricRelationTB.c.machine_id ).where( FabricRelationTB.c.fabric_id == (self.fabric)['id'] )
            proxy = conn.execute(stmt).fetchall()
            res = [dict(x) for x in proxy]
        except Exception as e:
            res = {}
        finally:
            conn.close()

        return res

    def copyToRemote(self):
        api.run("mkdir -p {remoteaddress}".format(remoteaddress=self.remoteaddress))
        return api.put(self.filepath, self.fullpath)

    def extraceCode(self):
        api.run("mkdir -p {deployaddress}".format(deployaddress=self.deployaddress))
        api.run("mkdir -p {deploy}".format(deploy=self.deployaddress))
        return api.run("tar -zxvf {file} -C {dest}".format( file = self.fullpath, dest=self.deployaddress ))

    def removeCode(self):
        return api.run(" rm -rf {file} ".format( file=self.fullpath ))

    def powerControl(self):
        return api.run("chown www-data.www-data -R {deployaddress}".format(deployaddress=self.deployaddress))



