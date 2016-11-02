#!/usr/bin/env python
# -*- coding:utf-8 -*-

import functools
import json

def authenticatedAjax(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            return self.write(json.dumps({
                'status': 'logout',
                'msg': 'needLogin'
            }))
        return method(self, *args, **kwargs)

    return wrapper