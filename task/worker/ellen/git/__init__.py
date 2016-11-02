#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygit2 import Repository

def is_repository(path):
    try :
        Repository(path)
        return True
    except KeyError:
        return False
