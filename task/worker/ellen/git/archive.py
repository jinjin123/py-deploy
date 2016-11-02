#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tarfile

def archve(repository, savepath):
    with tarfile.open( savepath, 'w:gz' ) as ar :
        repository.write_archive(repository.head.target, ar)