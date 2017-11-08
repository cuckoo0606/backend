#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Author: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-06-01


import time
import json
import datetime
from bson import ObjectId
from framework.web import paging
from tornado.util import ObjectDict
from framework.mvc.web import RequestHandler
from framework.data.mongo import db, Document
try:
    from settings import MAX_DAYS
except:
    MAX_DAYS = 15


class HandlerBase(RequestHandler):

    def initialize(self):
        id = self.get_current_user()
        current_user = self.redis_cache("user", id)
        self.context.current_user = current_user
        self.context.paging = paging.parse(self)
	self.context.func_time = self.func_time

    def get_current_user(self):
        token = self.get_secure_cookie("u")
        if not token:
            return None
        c = self.cache.get("LOGIN_TOKEN:" + token)
        if c is not None:
            info = json.loads(c)
            return info["user_id"]

    def json(self, obj, content_type="text/json; charset=utf-8", cls=None):
        """
            输出json结果
        """
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls).replace("</", "<\\/"))

    
    def system_record(self, user, logtype, operation, content):
        """
            搜集系统异常并写入系统日志
            字段:
                用户
                类型 0(系统错误) 1(登陆记录) 2(用户操作[增删改])
                模块
                操作
                内容
                时间 
                IP
        """
        path = self.get_template_name()
        ip = self.request.remote_ip

        log = Document()
        log.user = user
        log.logtype = logtype
        log.module = "templates/" in path and path.split("templates/")[1] or path
        log.operation = operation
        log.content = content
        log.createtime = datetime.datetime.now()
        log.ip = ip

        db.systemlog.save(log)

    def redis_cache(self, key, value):
        '''
            在缓存找到结果
            添加userid, username, roleid, permission
        '''
        result = None
        redis_key = "{0}:{1}".format(key, value)
        result = self.cache.get(redis_key)
        if key == "user":
            if not result:
                result = db.user.find_one({'_id': ObjectId(value)})
            else:
                result = ObjectDict(eval(result))
        elif key == "systemconfig":
            if not result:
                result = db.systemconfig.find_one({ "key": value })
                if result:
                    result = ObjectDict(result)
                    self.cache.set(redis_key, result, ex=3600)
            else:
                result = ObjectDict(eval(result))
        return result

    def set_cache(self, key, value):
        """
            主动更新缓存
        """
        redis_key = "{0}:{1}".format(key, value)
        if key == "systemconfig":
            result = db.systemconfig.find_one({ "key" : value })
            if result:
                self.cache.set(redis_key, ObjectDict(result), ex=3600)
                return True
        return False
    
    def select_time(self, time_type, starttime, endtime, deltahours):
        ''' 
            根据传入的本地开始时间和结束时间, 转为utc时间的带毫秒的时间戳, 并返回一个字典
            time_type: timestamp和datetime
        '''
        import calendar
        result = {}
        delta = datetime.timedelta(hours=deltahours)
        if starttime:
            select_start = self.time_format(starttime, ":00") - delta
            if time_type == "timestamp":
                select_start = calendar.timegm(select_start.utctimetuple()) * 1000
            result["$gte"] = select_start
        if endtime:
            select_end = self.time_format(endtime, ":00") - delta
            if time_type == "timestamp":
                select_end = calendar.timegm(select_end.utctimetuple()) * 1000
            result["$lt"] = select_end
        return result

    def time_format(self, time, suffix):
        '''
            时间字符串转为时间格式
        '''
        return datetime.datetime.strptime(time + suffix, "%Y-%m-%d %H:%M:%S")

    def is_rendering(self, starttime, endtime, type="default"):
        '''
            通过时间判断, 是否在页面渲染数据
            如果参数不齐全, 则直接返回
            如果不是管理员, 限制查询时间
        '''
        rendering = True
        if not starttime or not endtime:
            rendering = False
        else:
            if type == "day":
                select_start = self.time_format(starttime, " 00:00:00")
                select_end = self.time_format(endtime, " 00:00:00")
            else:
                select_start = self.time_format(starttime, ":00")
                select_end = self.time_format(endtime, ":00")
            days = (select_end - select_start).days
            if days > MAX_DAYS:
                rendering = False

        if not rendering:
            today = self.get_date(type)
            self.context.starttime = today['starttime']
            self.context.endtime = today['endtime']
            self.context.show = False
        else:
            self.context.starttime = starttime
            self.context.endtime = endtime
            self.context.show = True

        return rendering

    def get_date(self, type="default"):
        '''
            获取当天时间
        '''
        if type == "day":
            starttime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            endtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        else:
            starttime = time.strftime('%Y-%m-%d',time.localtime(time.time())) + " 00:00"
            endtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))    

        result = {"starttime" : starttime, "endtime" : endtime}

        return result

    def func_time(self, time, delta_hours=0):
        delta = datetime.timedelta(hours=delta_hours)
        result = (time + delta).strftime("%Y-%m-%d %H:%M:%S")

        return result
