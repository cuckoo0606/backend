#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Author: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-06-01


import os
import sys
import json
import datetime
import tornado.web
from bson import ObjectId
from core.web import HandlerBase
from framework.mvc.web import url
from framework.data.mongo import db
from framework.util.codes import error_code
from framework.util.mail import sendEmail

sys.path.append(os.path.abspath("../"))
reload(sys)
sys.setdefaultencoding('utf-8')
from settings import SERVERS


@url("/v1/systemconfig")
class SystemConfig_v1(HandlerBase):
    """
        
       1, 配置各服务器的性能阈值  
       2, 接收与监控各服务器发送过来的信息
    """
    
    def get_redis(self, arg, name):
        return self.redis_cache("systemconfig", "{0}_{1}".format(arg, name))

    def save(self, name, type, subtype, level, content, subname):
        # 严重错误, 发送邮件或短信
        if level == 1:
            sendEmail("严重错误", content)
        db.warning.save({
            "name": subname,
            "type": type,
            "subtype": subtype,
            "level": level,
            "content": content,
            "created": datetime.datetime.now()
        })
        cmd = "echo {0} >> /var/log/traffic/{1}/{2}/warning.log".format(content, name, subname)
        os.system(cmd)
        

    def get(self):
        name = self.get_argument('name', '')
        if not name:
            return self.json(error_code("NAME_NOT_NONE"))

        names = ['litai', 'zhonghui', 'jinma', 'lianyi', 'aifu', 'xinghui', 'weinuo', \
                'baoli', 'chaoxiang', 'laisi', 'test']
        types = ['wx', 'hq', 'api', 'cpu', 'men', 'disk']

        if name not in names:
            return self.json(error_code("RECORD_NOT_EXIST"))

        data = {}
        for i in types:
            arg = i + '_' + name
            k = db.systemconfig.find_one({'key': arg})
            data[i] = k and k['value'] or 0
            
        return self.json(data)

    def post(self):
        name = self.get_argument('name', '')
        subname = self.get_argument('subname', '')
        arg = self.get_argument('arg', '')

        if not name or not subname or not arg:
            return self.json(error_code("NAME_NOT_NONE"))
        # 判断路径是否存在
        dir_path = "/var/log/traffic/{0}/{1}".format(name, subname)
        if not os.path.exists(dir_path):
            os.system('mkdir -p {0}'.format(dir_path))
        # 解析参数, 获取CPU, 内存, 磁盘的使用率
        args = arg.split("-")
        # 系统性能
        if len(args) == 3:
            cpu = str(round(float(args[0]), 2))
            mem = str(round(float(args[1]), 2))
            disk = str(round(float(args[2]), 2))
            # 记录
            system_infos = '{' + '"cpu":' + cpu + ',' + '"mem":' + mem + ',' + '"disk":' + disk + '}'
            path = "{0}/system_infos.log".format(dir_path)
            cmd = "echo {0} >> {1}".format(json.dumps(system_infos), path)
            os.system(cmd)
            # 阈值预警
            m_cpu = self.get_redis("cpu", name)
            m_men = self.get_redis("men", name)
            m_disk = self.get_redis("disk", name)
            if float(cpu) > m_cpu.value:
                content = "CPU预警: 使用率为{0}%, 超过预警阈值{1}%".format(cpu, m_cpu.value)
                self.save(name, 1, "cpu", 3, content, subname)
            if float(mem) > m_men.value:
                content = "内存预警: 使用率为{0}%, 超过预警阈值{1}%".format(mem, m_men.value)
                self.save(name, 1, "mem", 3, content, subname)
            if float(disk) > m_disk.value:
                content = "磁盘预警: 使用率为{0}%, 超过预警阈值{1}%".format(disk, m_disk.value)
                self.save(name, 1, "disk", 3, content, subname)
        # 业务性能
        elif len(args) == 2 and args[0] in ['wx', 'hq', 'api']:
            new_arg = self.get_redis(args[0], name)
            keys = {
                'wx': '微信',
                'api': 'API',
                'hq': '行情'
            }
            # 记录
            info = '\'{' + '"' + args[0] + '"'  + ':' + args[1] + '}\''
            path = "{0}/{1}.log".format(dir_path, args[0])
            cmd = "echo {0} >> {1}".format(info, path)
            os.system(cmd)
            # 阈值预警
            if int(args[1]) > new_arg.value:
                content = "{0}预警: 每分钟访问量为{1}次, 超过预警阈值{2}次".format(keys[args[0]], args[1], new_arg.value)
                self.save(name, 2, args[0], 3, content, subname)
        # MONGODB状态
        elif len(args) == 1 and args[0] == "error":
            path = "{0}/{1}.log".format(dir_path, "mongo")
            content = "{0}, 服务器: {1},  数据库连接失败!".format(self.func_time(datetime.datetime.now()), SERVERS[subname])
            cmd = "echo {0} >> {1}".format(content, path)
            os.system(cmd)
            self.save(name, 3, 'mongo', 1, content, subname)
        # 其他类型
        else:
            return self.json(error_code("ARG_ERROR"))
            



@url("/v1/getip")
class GetIp_v1(HandlerBase):
    """
        获取访问IP
    """
    def get(self):
        ip = self.request.remote_ip
        return self.write(ip)
