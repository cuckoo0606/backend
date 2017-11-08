# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor:
# Email:
# Create Date: 2017-07-26 16:04:11


import os
import json
import psutil
import datetime
import tornado.web
import tornado.ioloop

from settings import *


class SystemInfosHandler(tornado.web.RequestHandler):

    def json(self, obj, content_type="text/json; charset=utf-8", cls=None):
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls).replace("</", "<\\/"))

    def get(self):
        '''
            获取cpu使用率, 内存信息
        '''
        # cpu平均使用率
        p1 = psutil.cpu_percent(interval=None, percpu=False)
        # 每个cpu使用率
        p2 = psutil.cpu_percent(interval=None, percpu=True)

        # 内存信息
        m = psutil.virtual_memory()
        # 总内存
        total_m = int(round(m.total/1024/1024/1024))
        # 内存使用率
        #pre_m = m.percent
        pre_m = psutil.virtual_memory().percent
        # 磁盘信息
        disk_infos = []
        disk = psutil.disk_partitions()
        for i in disk:
            usage = psutil.disk_usage(i.mountpoint)
            info = '磁盘: {0}, 挂载点: {1}, 总空间: {2}G, 可用空间: {3}G, 使用率: {4}%'.format(i.device, \
                    i.mountpoint, usage.total/1024/1024/1024, usage.free/1024/1024/1024, usage.percent)
            disk_infos.append(info)

        result = {}
        result['systemname'] = SYSTEM_NAME
        result["totalCpu"] = str(p1) + '%'
        result["eachCpu"] = [ str(i)+'%' for i in p2 ]
        result["totalMemory"] = str(total_m) + 'G'
        result["memoryUsage"] = str(pre_m) + '%'
        result["cpuCount"] = psutil.cpu_count(logical=True)
        result['diskInfos'] = disk_infos
        result["starttime"] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        result["mark"] = "totalCpu: 总CPU使用率, eachCpu: 每个cpu使用率, totalMemory: 总内存大小(G), \
                memoryUsage: 内存使用率, cpuCount: cpu核数, starttime: 服务器启动时间"

        return self.json({"status": 0, "data": result})

    def post(self):
        return self.write('sfsdf')


class ReloadBotsHandler(tornado.web.RequestHandler):

    def get(self):
        '''
            重启后台
        '''
        try:
            for i in BOTS:
                os.system('pm2 reload {0}'.format(i))

            return self.write('重启后台成功')
        except:
            return self.write('重启后台出现异常')


class ReloadWXHandler(tornado.web.RequestHandler):

    def get(self):
        '''
            重启微信
        '''
        try:
            for i in WX:
                os.system('pm2 reload {0}'.format(i))

            return self.write('重启微信成功')
        except:
            return self.write('重启微信出现异常')


class ReloadFountainHandler(tornado.web.RequestHandler):

    def get(self):
        '''
            重启行情
        '''
        os.system('pm2 reload fountain')
        return self.write('重启行情成功')


def make_app():
    return tornado.web.Application([
        (r"/v1/query/systeminfos", SystemInfosHandler),
        (r"/v1/reload/bots", ReloadBotsHandler),
        (r"/v1/reload/wx", ReloadWXHandler),
        (r"/v1/reload/fountain", ReloadFountainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(3001)
    tornado.ioloop.IOLoop.current().start()
