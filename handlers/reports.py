# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor: cuckoo
# Email: skshadow0606@@gmail.com
# Create Date: 2017-06-02 11:59:17


import re
import os
import pymongo
import datetime
import tornado.web
from bson import ObjectId
from core.web import HandlerBase
from framework.web import paging
from framework.mvc.web import url
from framework.util.codes import error_code
from framework.data.mongo import db, DBRef, Document

@url("/reports/mt4")
class MT4(HandlerBase):
    
    @tornado.web.authenticated
    def get_where(self, starttime, endtime, status):
        where = {}
        if status != -1:
            where['type'] = status
        select_time = self.select_time("datetime", starttime, endtime, 8)
        where['created'] = select_time
        return where


    @tornado.web.authenticated
    def get(self):
        starttime = self.get_argument("starttime", "")
        endtime = self.get_argument("endtime", "")
        status = self.get_argument('status', "-1")
        self.context.status = status
        self.context.mt4s = {}
        rendering = self.is_rendering(starttime, endtime)
        if not rendering:
            return self.template()
    
        where = self.get_where(starttime, endtime, int(status))
        self.context.paging = paging.parse(self)
        self.context.mt4s = db.mt4.find(where).sort([("created", -1)]) \
            .skip(paging.skip(self.context.paging)) \
            .limit(self.context.paging.size)
        self.context.paging.count = self.context.mt4s.count()

        return self.template()


