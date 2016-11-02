#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygit2

def create_tag(repository, name, tagger, message):
    oid = repository.create_tag(name, str(repository.head.target), pygit2.GIT_OBJ_COMMIT, tagger, message)
    return oid
