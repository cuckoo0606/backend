# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-11-10 16:50:43


import os
import sys
import time
import smtplib
from email.mime.text import MIMEText

sys.path.append(os.path.abspath("../../"))
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    from settings import MAIL_FROM, MAIL_PWD, MAIL_TO, MAIL_LOG_PATH
except:
    MAIL_FROM = "454045250@qq.com"
    MAIL_PWD = "rfucqvfcuucecbca"
    MAIL_TO = ["wangyangsheng@sofyun.com","hongyi@sofyun.com"]
    MAIL_LOG_PATH = "/var/log/mail/"


# 错误日志路径
ERROR_PATH = "{0}{1}".format(MAIL_LOG_PATH, "error.log")
ACCESS_PATH = "{0}{1}".format(MAIL_LOG_PATH, "access.log")


def sendEmail(title, content):
    for i in MAIL_TO:
        msg = MIMEText(content)
        msg["Subject"] = title
        msg["From"] = MAIL_FROM
        msg["To"] = i
        ps = "邮件发送{0}: 主题=> {1}, 内容=> {2}, 异常=> {3}"

        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(MAIL_FROM, MAIL_PWD)
            s.sendmail(MAIL_FROM, i, msg.as_string())
            s.quit()
            time.sleep(1)
            new_ps = ps.format("成功", title, content, "无")
            cmd = "echo '{0}' >> {1}".format(new_ps, ACCESS_PATH)
            print "Success!"
        except Exception, e:
            new_ps = ps.format("失败", title, content, str(e))
            cmd = "echo '{0}' >> {1}".format(new_ps, ERROR_PATH)
            print "Falied,%s"%str(e)
        os.system(cmd)


if __name__ == '__main__':
    title = "服务器异常"
    content = "测试环境错误，请立即维护!"
    sendEmail(title, content)
