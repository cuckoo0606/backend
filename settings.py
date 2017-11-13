#!/usr/lib/env python
#-*- encoding:utf-8 -*-

# Author: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-06-01


#
# MongoDB设置
#
# MongoDB地址
MONGODB_HOST = "127.0.0.1"
# MongoDB端口
MONGODB_PORT = 27017
# MongoDB库名
MONGODB_DB = "sofyun"
MONGODB_USER = ''
MONGODB_PASSWORD = ''


#
# WebServer设置
#

# WebServer端口
TORNADO_PORT = 8080
# COOKIE加密匙
COOKIE_SECRET = "61oETzKXQAGaYkljksYUHGjSQJmjuGf1o/Vo="
# 登陆页面
LOGIN_URL = "/account/signin"


#
# 页面设置
#

# 默认分页每页大小
DEFAULT_PAGESIZE = 10


#
# 邮件配置
#

# 发送人(QQ邮箱)
MAIL_FROM = "454045250@qq.com"
# 密钥
MAIL_PWD = "rfucqvfcuucecbca"
# 接收着(列表)
MAIL_TO = ["hongyi@sofyun.com"]
#MAIL_TO = ["wangyangsheng@sofyun.com","hongyi@sofyun.com"]
# 日志路径
MAIL_LOG_PATH = "/var/log/mail/"
# 
# 发送等级
#
# 1: 严重错误
# :
MAIL_LEVEL = [1]


#
# 服务器名称
#

SERVERS = {
    "zhonghui": "中汇",
    "zhonghuihq": "中汇行情",
}
