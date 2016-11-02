#!/usr/bin/env python
# -*- coding:utf-8 -*-

from library.handlers import BaseHandler
from library.route import route
from models.Machine import MachineModel
from library.decorators import authenticatedAjax
from library.utils import Utils

@route(r'/machine/view/(.+)')
class MachineviewHandler( BaseHandler ):
    def get(self, view , *args, **kwargs):
        self.render('machine/' + view + '.html')

@route(r'/machine/add')
class MachineaddHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        name = self.get_argument('name', default=None)
        account = self.get_argument('account', default=None)
        password = self.get_argument('password', default=None)
        desc = self.get_argument('desc', default=None)
        ip = self.get_argument('ip', default=None)
        auth_type = self.get_argument('auth_type', default='password', strip=True)

        res = MachineModel().addMachine( name = name,
                                         account = account,
                                         password = password,
                                         desc = desc,
                                         ip=ip,
                                         auth_type=auth_type
                                         )

        self.ajax(res)

@route(r'/machine/list')
class MachinelistHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, *args, **kwargs):
        project_id = self.get_argument('project', default=None)
        res = MachineModel().getMachines(project_id=project_id)
        data = res['data']
        for x in range(len(data)):
            if data[x]['auth_type'] == 'key':
                data[x]['password'] = '-'

            data[x]['create_time'] = Utils.timeformat(data[x]['create_time'])

        res['data'] = data
        self.ajax(res)

@route(r'/machine/del')
class MachinedelHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        machine = self.get_argument('machine', default=None)
        res = MachineModel().delMachines(machine)
        self.ajax(res)


@route(r'/machine/project/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})')
class MachineprojectHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, project_id, *args, **kwargs):
        res = MachineModel().getMachineByProject(project_id)
        self.ajax(res)

@route(r'/machine/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})')
class MachineviewHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, machine_id):
        res = MachineModel().getMachineInfo(machine_id=machine_id)
        self.ajax(res)

@route(r'/machine/edit')
class MachineeditHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        id = self.get_argument('id', default=None, strip=None)
        name = self.get_argument('name', default=None, strip=None)
        account = self.get_argument('account', default=None, strip=None)
        password = self.get_argument('password', default=None, strip=None)
        desc = self.get_argument('desc', default=None, strip=None)
        ip = self.get_argument('ip', default=None, strip=None)
        auth_type = self.get_argument('auth_type', default=None, strip=None)

        res = MachineModel().editMachine(id=id, name=name, account=account, password=password, desc=desc, ip=ip, auth_type=auth_type)
        self.ajax(res)




