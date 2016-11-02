#!/usr/bin/env python
# -*- coding:utf-8 -*-

from library.handlers import BaseHandler
from library.route import route
from models.Fabric import FabricModel
from library.decorators import authenticatedAjax
from library.utils import Utils

@route(r'/fabric/view/(.+)')
class FabricviewHandler( BaseHandler ):
    def get(self, view , *args, **kwargs):
        self.render('fabric/' + view + '.html')

@route(r'/fabric/tag')
class FabrictagHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, *args, **kwargs):
        project = self.get_argument('project', default=None, strip=True)
        res = FabricModel().getTagByProject(project)
        self.ajax(res)

@route(r'/fabric/add')
class FabricaddHandler(BaseHandler):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        type = self.get_argument('type', default=None, strip=True)
        project = self.get_argument('project', default=None, strip=True)
        desc = self.get_argument('desc', default=None, strip=True)
        tag = self.get_argument('tag', default=None, strip=True)
        machine = self.get_argument('machine', default=None, strip=True)
        if machine:
            machine = machine.split(',')
        else :
            machine = []

        res = FabricModel().addFabric(
            type = type,
            project = project,
            desc = desc,
            tag = tag,
            machine = machine,

        )
        self.ajax(res)

@route(r'/fabric/edit')
class FabriceditHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        id = self.get_argument('fabric_id', default=None, strip=True)
        type = self.get_argument('type', default=None, strip=True)
        project = self.get_argument('project', default=None, strip=True)
        desc = self.get_argument('desc', default=None, strip=True)
        tag = self.get_argument('tag', default=None, strip=True)

        res = FabricModel().editFabric(
            id = id,
            type=type,
            project=project,
            desc=desc,
            tag=tag,
        )
        self.ajax(res)

@route(r'/fabric/list')
class FabriclistHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, *args, **kwargs):
        status = self.get_argument('status', default=None, strip=True)
        res = FabricModel().getFabrics(status)
        data = res['data']
        for x in range(len(data)):
            data[x]['fabric_time'] = Utils.timeformat(data[x]['fabric_time'])
            data[x]['finish_time'] = Utils.timeformat(data[x]['finish_time'])
        self.ajax(res)

@route(r'/fabric/ready')
class FabricreadyHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        fabric = self.get_argument('fabric', default=None, strip=True)
        res = FabricModel().setFabricToReady(fabric)
        self.ajax(res)

@route(r'/fabric/cancel')
class FabricreadyHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        fabric = self.get_argument('fabric', default=None, strip=True)
        res = FabricModel().setFabricToCalcel(fabric)
        self.ajax(res)

@route(r'/fabric/deploy')
class FabricdeployHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        fabric = self.get_argument('fabric', default=None, strip=None)
        res = FabricModel().deployProject(fabric)
        self.ajax(res)

@route(r'/fabric/machine/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})')
class FabricmachineHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, fabric_id):
        res = FabricModel().getFabricRelationMachines(fabric_id)
        self.ajax(res)

@route(r'/fabric/addmachine')
class FabricaddmachineHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        fabric_id = self.get_argument('fabric_id', default=None , strip=None)
        machine_id = self.get_argument('machine_id', default=None , strip=None)
        res = FabricModel().addMachineToFabric(fabric_id, machine_id)
        self.ajax(res)

@route(r'/fabric/delmachine')
class FabricdelmachineHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        fabric_id = self.get_argument('fabric_id', default=None , strip=None)
        machine_id = self.get_argument('machine_id', default=None , strip=None)
        res = FabricModel().delMachineToFabric(fabric_id, machine_id)
        self.ajax(res)

@route(r'/fabric/viewmachine/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})')
class FabricviewmachineHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, fabric_id):
        res = FabricModel().allMachinesByFabric(fabric_id)
        data = res['data']
        for x in range(len(data)):
            fabric_time = data[x]['fabric_time']
            data[x]['fabric_time'] = Utils.timeformat(data[x]['fabric_time'])

            finish_time = data[x]['finish_time']
            data[x]['finish_time'] = Utils.timeformat(data[x]['finish_time'])

            data[x]['expend'] = '-'
            if fabric_time and finish_time :
                data[x]['expend'] = finish_time - fabric_time
                data[x]['expend'] = str(data[x]['expend']) + '秒'

        self.ajax(res)

@route(r'/fabric/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})')
class FabricinfoHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, fabric_id):
        res = FabricModel().getFabricInfoById(fabric_id)

        self.ajax(res)

@route(r'/fabric/usabletag')
class fabrictagHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, *args, **kwargs):
        self.ajax( FabricModel.getUsableTag() )