# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-07-27 16:55:09
;;;;
:wq


import os
import json
import requests
import psutil
import datetime
import tornado.web
import tornado.ioloop

from settings import *

projects = ['wx', 'bots', 'fountain']


class ReloadHandler(tornado.web.RequestHandler):

    def json(self, obj, content_type="text/json; charset=utf-8", cls=None):
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls).replace("</", "<\\/"))

    def get(self):
        customer = self.get_argument('customer', '')
        project = self.get_argument('project', '')

        if not customer:
            return self.json({'status': -1, 'msg': '缺少客户名称'})
        elif customer not in customers:
            return self.json({'status': -2, 'msg': '没有此客户资料'})

        if not project:
            return self.json({'status': -1, 'msg': '缺少项目名称'})
        elif project not in projects:
            return self.json({'status': -2, 'msg': '没有此项目资料'})

        url = 'http://{0}:3001/v1/reload/{1}'.format(customers[customer], project)
        try:
            r = requests.get(url, timeout=10)
            return self.json({'status': 0, 'msg': '重启成功'})
        except:
            return self.json({'status': -99, 'msg': '连接失败'})

        

class SystemInfosHandler(tornado.web.RequestHandler):

    def json(self, obj, content_type="text/json; charset=utf-8", cls=None):
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls).replace("</", "<\\/"))
    
    def get(self):
        customer = self.get_argument('customer', '')

        if customer not in customers:
            return self.json({'status': -2, 'msg': '没有此客户资料'})

        url = 'http://{0}:3001/v1/query/systeminfos'.format(customers[customer])
        try:
            r = requests.get(url, timeout=10)
            return self.json(r.json())
        except:
            print 'error'


def make_app():
    return tornado.web.Application([
        (r"/v1/reload", ReloadHandler),
        (r"/v1/query/systeminfos", SystemInfosHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(3001)
    tornado.ioloop.IOLoop.current().start()
