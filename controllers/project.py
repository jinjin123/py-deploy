#!/usr/bin/env python
# -*- coding:utf-8 -*-

from library.handlers import BaseHandler
from library.route import route
from library.utils import Utils
from models.Project import ProjectModel
from library.decorators import authenticatedAjax

@route(r'/project/view/(.+)')
class ProjectviewHandler( BaseHandler ):
    def get(self, view , *args, **kwargs):
        self.render('project/' + view + '.html')


@route(r'/project/add')
class ProjectaddHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        name = self.get_argument('name', default=None)
        desc = self.get_argument('desc', default=None)
        gituser = self.get_argument('gituser', default=None)
        gitaddress = self.get_argument('gitaddress', default=None)
        localaddress = self.get_argument('localaddress', default=None)
        remoteaddress = self.get_argument('remoteaddress', default=None)
        deployaddress = self.get_argument('deployaddress', default=None)

        project = ProjectModel()
        res = project.addProject(
            name = name ,
            gituser = gituser ,
            gitaddress = gitaddress ,
            localaddress = localaddress ,
            remoteaddress = remoteaddress ,
            deployaddress = deployaddress ,
            desc = desc
        )

        self.ajax(res)

@route(r'/project/edit')
class ProjecteditHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        id = self.get_argument('id', default=None)
        name = self.get_argument('name', default=None)
        desc = self.get_argument('desc', default=None)
        gituser = self.get_argument('gituser', default=None)
        gitaddress = self.get_argument('gitaddress', default=None)
        localaddress = self.get_argument('localaddress', default=None)
        remoteaddress = self.get_argument('remoteaddress', default=None)
        deployaddress = self.get_argument('deployaddress', default=None)

        res = ProjectModel().editProject(
            id = id ,
            name = name ,
            gituser = gituser ,
            gitaddress = gitaddress ,
            localaddress = localaddress ,
            remoteaddress = remoteaddress ,
            deployaddress = deployaddress ,
            desc = desc
        )

        self.ajax(res)

@route(r'/project/list')
class ProjectlistHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, *args, **kwargs):
        status = self.get_argument('status', default=None, strip=True)
        res = ProjectModel().getAllProject(status)

        data = res['data']
        for x in range(len(data)):
            data[x]['create_time'] = Utils.timeformat(data[x]['create_time'])

        self.ajax( res )

@route(r'/project/del')
class ProjectdelHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        projects = self.get_argument('projects', default=None)
        res = ProjectModel().delProjects(projects.split(','))
        self.ajax(res)

@route(r'/project/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})')
class ProjectinfoHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, project_id, *args, **kwargs):
        res = ProjectModel().getInfoByProjectId(project_id)
        self.ajax(res)

@route(r'/project/again')
class ProectagainHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        project = self.get_argument('project_id', default=None)
        res = ProjectModel().tryAgain(project)
        self.ajax(res)

@route(r'/project/relation/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})')
class ProjectrelationHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, project_id, *args, **kwargs):
        res = ProjectModel().getRelationMachines(project_id)
        self.ajax(res)

@route(r'/project/relation/add')
class ProjectrelationaddHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        project = self.get_argument('project', default=None)
        machine = self.get_argument('machine', default=None)
        machine = machine.split(',')

        res = ProjectModel().addRelation(project, machine)
        self.ajax(res)

@route(r'/project/relation/del')
class ProjectrelationdelHandler( BaseHandler ):
    @authenticatedAjax
    def post(self, *args, **kwargs):
        project = self.get_argument('project', default=None)
        machine = self.get_argument('machine', default=None)
        machine = machine.split(',')

        res = ProjectModel().delRelation(project, machine)
        self.ajax(res)

@route(r'/project/detail/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12,})/(.*)')
class ProjectdetailHandler( BaseHandler ):
    @authenticatedAjax
    def get(self, project, path, *args, **kwargs):
        print(project)
        print(path)
        pro = ProjectModel()
        self.ajax( pro.getList(project, path) )
