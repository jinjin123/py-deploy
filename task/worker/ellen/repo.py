#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygit2 import Repository
from pygit2 import Signature
from . git.clone import clone_repository
from . git.auth import auth
from . git.tag import create_tag
from . git.pull import pull
from . git.archive import archve
from . utils import JagareError


class Jagare(object):
    ''' pygit2 and git commands wrapper '''

    def __init__(self, path):
        self.repository = repository(path)
        self.repository_name = None

    def __eq__(self, other):
        if isinstance(other, Jagare):
            return self.path == other.path
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.path)

    @property
    def path(self):
        return self.repository.path

    @property
    def empty(self):
        return self.repository.is_empty

    @property
    def bare(self):
        return self.repository.is_bare

    @property
    def head(self):
        """ return pygit2.Reference """
        # FIXME: return repo.head.name ?
        if self.repository.is_empty:
            return None
        return self.repository.head

    @staticmethod
    def clone(url, path, bare=False, repository=None, remote=None, checkout_branch=None, callbacks=None):
        try:
            clone_repository(url, path, bare=bare, repository=repository, remote=remote, checkout_branch=checkout_branch, callbacks=callbacks)
        except Exception as e:
            raise e

    @staticmethod
    def auth(username=None, pubkey=None, privkey=None, password=None ):
        return auth( username=username, pubkey=pubkey, privkey=privkey, password=password )

    def pull(self, remote_name='origin', callbacks=None):
        return pull(self.repository, remote_name=remote_name, callbacks=callbacks)

    def archive(self, savepath):
        return archve(self.repository, savepath=savepath)

    @staticmethod
    def tagger(username, email):
        return Signature(username, email)

    def create_tag(self, tag, message, username, email):
        # name, oid, type, tagger, message
        return create_tag(self.repository, tag, Jagare.tagger(username, email), message)

def repository(path):
    try:
        repo = Repository(path)
    except KeyError:
        raise JagareError('repo %s not exists' % path)
    return repo


