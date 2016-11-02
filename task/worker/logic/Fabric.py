#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import os.path
import os
from conf import conf
from logic.Base import BaseModel
from logic.Deploy import DeployModel
from mapping import fabric_engine
from mapping.Project import ProjectTB
from mapping.FabricRelation import FabricRelationTB
from sqlalchemy.sql import select
from ellen.repo import Jagare
from mapping.Fabric import FabricTB

from . import Singleton

class FabricModel( BaseModel ):
    __metaclass__ = Singleton

    def _getFabricInfo(self, fabric_id):
        conn = fabric_engine.connect()
        try:
            stmt = select([FabricTB]).where( FabricTB.c.id == fabric_id )
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0:
                res = dict( proxy.fetchone() )
            else :
                res = {}
        except Exception as e:
            res = {}
        finally:
            conn.close()

        return res

    def _getProjectInfo(self, project_id):
        conn = fabric_engine.connect()
        try:
            stmt = select([ProjectTB]).where(ProjectTB.c.id == project_id)
            proxy = conn.execute(stmt)
            if proxy.rowcount > 0:
                res = dict(proxy.fetchone())
            else:
                res = {}
        except Exception as e:
            res = {}
        finally:
            conn.close()

        return res

    def _endFabric(self, fabric_id, status,fabric_time, finish_time, error=None, success_num=0, error_num=0):
        conn = fabric_engine.connect()
        try:
            stmt = FabricTB.update().values(status=status, fabric_time=fabric_time, finish_time=finish_time, error=error, success_num=success_num, error_num=error_num).where(FabricTB.c.id == fabric_id)
            conn.execute(stmt)
        except Exception as e:
            pass
        finally:
            conn.close()

    def _setMachinesStatus(self, fabric_id, status):
        conn = fabric_engine.connect()
        try:
            upstmt = FabricRelationTB.update().values( status = status ).where( FabricRelationTB.c.fabric_id == fabric_id )
            conn.execute(upstmt)
            res = True
        except Exception as e:
            res = False
        finally:
            conn.close()

        return res

    @staticmethod
    def deployFabric(payload):
        # step.1 fetch and merge
        # step.2 export this code with tar.gz
        # step.3 update this archive.tar.gz to aliyun'oss
        # step.4 deploy this code with each machine and update each machine's status
        # step.5 update this fabric's status.
        fabric_id = payload.get('fabric_id', None)
        fabricobj = FabricModel()
        fabric_info = fabricobj._getFabricInfo( fabric_id )
        fabric_time = int( time.time() )
        if fabric_info :
            # get logger obj
            logger = BaseModel.getLogger(fabric_info['id'], 'fabric')
            logger.info("获取到发布计划")
            project_info = fabricobj._getProjectInfo( fabric_info['project_id'] )
            if project_info:
                logger.info("获取到任务信息")
                # savepath, localpath, fabric_time, tag, mode='tar.gz'
                savepath = BaseModel.buildpath(conf.savepath,
                                               project_info['localaddress'],
                                               fabric_info['create_time'],
                                               fabric_info['tag'],
                                               )  # export git tar.gz file

                if fabric_info['type'] == 'new':
                    try:
                        logger.info("开始创建Git对象")
                        git = Jagare(project_info['localaddress'])
                        logger.info("git对象创建成功")
                    except Exception as e:
                        logger.info("git对象创建失败:" + str(e))
                        fabricobj._endFabric(
                            fabric_id,
                            'error',
                            fabric_time,
                            int(time.time()),
                            str(e)
                        )
                        return 'end'

                    # step.1
                    try:
                        logger.info("开始更新代码")
                        git.pull(callbacks=git.auth(project_info['gituser'], conf.auth.pubkey, conf.auth.privkey, ''))
                        logger.info("代码更新成功")
                    except Exception as e:
                        logger.info("代码更新失败:" + str(e) )
                        fabricobj._endFabric(
                            fabric_id,
                            'error',
                            fabric_time,
                            int(time.time()),
                            str(e)
                        )

                    # step.2
                    try:
                        logger.info("开始导出代码")
                        dirname = os.path.dirname(savepath)
                        if not os.path.exists(dirname) :
                            os.makedirs(dirname)
                        git.archive(savepath)
                        logger.info("代码导出成功")
                    except Exception as e:
                        logger.info("代码导出失败" + str(e))
                        fabricobj._endFabric(
                            fabric_id,
                            'error',
                            fabric_time,
                            int(time.time()),
                            str(e)
                        )
                        return 'end'

                    # step.2.5
                    # create tag for this repo
                    try:
                        logger.info("开始给Git仓库打标签")
                        git.create_tag(
                            fabric_info['tag'],
                            fabric_info['desc'],
                            conf.username,
                            conf.email
                        )
                        logger.info("Git标签添加成功")
                    except Exception as e:
                        logger.info("标签添加失败" + str(e))

                    # step.3
                    try:
                        logger.info("开始上传至OSS")
                        osspath = BaseModel.buildOssPath(project_info['localaddress'], fabric_info['create_time'], fabric_info['tag'])
                        logger.info( 'OSS地址为:' + osspath)
                        BaseModel.uploadFileToOss( local=savepath, remote=osspath )
                        logger.info("OSS上传成功")
                    except Exception as e:
                        logger.info("OSS上传失败" + str(e))

                #step.4
                try:
                    logger.info("开始进行发布对象构建")
                    if os.path.exists(savepath):
                        res = DeployModel(fabric_info, project_info , savepath).deployMachineByFabric()
                    else :
                        raise FileNotFoundError("没有找到对应的发布包")
                    logger.info("发布过程结束")
                except FileNotFoundError as e:
                    logger.info("发布过程异常:" + str(e))
                    fabricobj._endFabric(
                        fabric_id,
                        'error',
                        fabric_time,
                        int(time.time()),
                        str(e)
                    )
                    fabricobj._setMachinesStatus(fabric_id, 'error')
                    return 'end'
                except Exception as e:
                    logger.info("发布过程异常" + str(e))
                    fabricobj._endFabric(
                        fabric_id,
                        'error',
                        fabric_time,
                        int(time.time()),
                        str(e)
                    )
                    return 'end'

                #step.5
                finish_time = int( time.time() )
                fabricobj._endFabric(fabric_id, 'end', fabric_time, finish_time, success_num=res['success'], error_num=res['error'])
                logger.info("发布结束")
            else:
                # not found project'info
                logger.info("没有获取到项目信息")
                fabricobj._endFabric(
                    fabric_id,
                    'error',
                    fabric_time,
                    int(time.time()),
                    'not found project'
                )

        else :
            # not found fabric'info
            print("没有获取到发布计划")


        return 'end'

