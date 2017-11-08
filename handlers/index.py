# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor: cuckoo
# Email: skshadow0606@@gmail.com
# Create Date: 2017-06-02 11:59:17


import tornado.web
from core.web import HandlerBase
from framework.mvc.web import url
from framework.data.mongo import db


@url("/index")
class Index(HandlerBase):

    @tornado.web.authenticated
    def get(self):
        return self.template()
