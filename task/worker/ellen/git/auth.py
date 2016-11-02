#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygit2 import Keypair, RemoteCallbacks

def auth( username=None, pubkey=None, privkey=None, password=None ):
    credentials = Keypair(username=username, pubkey=pubkey, privkey=privkey, passphrase=password)
    return RemoteCallbacks( credentials = credentials )

