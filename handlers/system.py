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

@url("/system/config")
class SystemConfig(HandlerBase):
    
    @tornado.web.authenticated
    def get(self):
        self.context.systemconfigs = [ c for c in db.systemconfig.find() ]
        return self.template()


@url("/config/(?P<key>[^/]+)/(?P<value>.+)")
class SystemConfigSet(HandlerBase):

    @tornado.web.authenticated
    def get(self, key, value):
        res_int = r"^\d+$"
        res_float = r"^\d+(\.\d+)?$"
	
	# 浮点型
	if "cpu_" in key or "men_" in key:
	    if not re.match(res_float, value):
		return self.json(error_code("INVALID_FORMAT"))
	    value = float(value)
        # 整型
	elif "api_" in key or "hq_" in key or "wx_" in key or "disk_" in key:
	    if not re.match(res_int, value):
		return self.json(error_code("INVALID_FORMAT"))
	    value = int(value)
	else:
	    return self.json(error_code("REFEREE_ERROR"))

        conf = db.systemconfig.find_one({ "key" : key })
        try:
            if conf:
                db.systemconfig.update({ "key" : key }, { "$set" : { "value" : value } })
            else:
                db.systemconfig.save({ "key" : key, "value" : value })
            
            result = self.set_cache("systemconfig", key)
            if not result:
                self.system_record("系统", 0, "系统设置", "更新缓存失败")

            current_user = self.context.current_user
            self.system_record(current_user._id, 3, "系统设置", "")
            return self.json({ "status" : "ok" })
        except Exception, e:
            print e
            self.system_record("系统", 0, "系统设置", e.message)
            return self.json(error_code("UNKNOW_ERROR"))
