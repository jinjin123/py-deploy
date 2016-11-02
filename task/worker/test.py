#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ellen.git.clone import clone_repository
from ellen.utils.auth import auth

result = clone_repository( 'bingo@git.hilava.net:/git/bingo.git', '/root/bingo',
                           bare=True,
                           callbacks=auth('bingo','/root/.ssh/id_rsa.pub', '/root/.ssh/id_rsa','')
                  )

if result:
    print "本地仓库创建成功"
else :
    print "本地仓库创建失败"