# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-08-03 11:34:27


# 需要删除的日志路径
LOG_LISTS = ['/var/log/nginx/q.log', '/var/log/nginx/q.log.1']
# 系统名称
SYSTEM_NAME = '朝向财富主服务器'
# 后台
BOTS = ['web-'+i for i in  map(str, range(8001, 8009))]
# 微信
WX = ['wx-'+i for i in  map(str, range(7001, 7009))]
