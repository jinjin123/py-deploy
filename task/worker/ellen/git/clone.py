#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygit2 import clone_repository as clone

def clone_repository(url, path, bare=False, repository=None, remote=None, checkout_branch=None, callbacks=None):
    clone(url, path, bare=bare, repository=repository, remote=remote, checkout_branch=checkout_branch, callbacks=callbacks)
