#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controllers import dashboard
from controllers import login
from controllers import main
from controllers import components
from controllers import machine
from controllers import project
from controllers import fabric

urls = []
urls.extend(dashboard.route.url_list)
urls.extend(main.route.url_list)
urls.extend(login.route.url_list)
urls.extend(components.route.url_list)
urls.extend(machine.route.url_list)
urls.extend(project.route.url_list)
urls.extend(fabric.route.url_list)
