#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-06-01


import tornado.web
from bson import ObjectId
import json
import random
from core.web import HandlerBase
from framework.mvc.web import url
from framework.data.mongo import db
from framework.util.security import md5


@url(["/account/signin", "/"])
class Signin(HandlerBase):

    def get(self):
        self.context.message = ""
        return self.template()

    def post(self):
        u = self.get_argument("user_id", "")
        p = self.get_argument("pwd", "")
        
        self.context.userid = u
        self.context.password = p

        p = md5(p)
        user = db.user.find_one({"user_id": u, "pwd": p})
        if user:
            token = "".join(random.sample("0123456789abcdefghijklmnopqrstuvwxyz", 32))
            v = json.dumps({"user_id": str(user._id)})
            self.cache.set("LOGIN_TOKEN:" + token, v, ex=3600)
            self.set_secure_cookie("u", token, expires_days=1)
            self.system_record(user._id, 1, "用户登陆", "")
            return self.redirect("/index")
        else:
            self.context.message = "用户名或密码错误"
            return self.template()
        return self.redirect('/index')


@url("/account/signout")
class Signout(HandlerBase):

    def get(self):
        user = self.context.current_user
        self.system_record(user._id, 1, "用户注销", "")
        token = self.get_secure_cookie("u")
        if token:
            self.cache.delete("LOGIN_TOKEN:" + token)
        self.clear_cookie("u")
        return self.redirect("/account/signin")
