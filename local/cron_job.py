# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-08-03 14:29:35


import os
import time
import datetime
import schedule
from settings import LOG_LISTS


'''
    执行定时任务并添加日志
'''


def remark(arg):
    '''
        备注
    '''
    created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = "{0} | {1}".format(arg, created)
    print msg
    log = 'echo "{0}" >> log.txt'.format(msg)
    os.system(log)


def backup():
    '''
        每天备份数据库, 保留最近三天的数据, 云Mongo的不用备份
    '''
    today = datetime.datetime.now()
    str_today = today.strftime('%Y%m%d')
    delta = datetime.timedelta(days=3)
    del_day = (today - delta).strftime('%Y%m%d')
    try:
        os.system('mongodump -d bots -o ~/db_bak/{0}'.format(str_today))
        remark('备份数据库成功 | {0}'.format(str_today))
        if os.path.exists('/root/db_bak/'+del_day):
            os.system('rm -rf /root/db_bak/{0}'.format(del_day))
            remark('成功删除数据库备份 | {0}'.format(del_day))
    except Exception as e:
        print e
        remark('出现异常: {0}'.format(e))


def clean():
    '''
	每周删除一次日志(主要是Nginx的行情日志)
    '''
    try:
        for i in LOG_LISTS:
            os.system('echo '' > {0}'.format(i))
            remark('已成功清除日志: {0}'.format(i))
    except Exception, e:
        print e
        remark('出现异常: {0}'.format(e))


if __name__ == "__main__":
    schedule.every().day.at('03:00').do(backup)
    schedule.every().saturday.at("04:00").do(clean)
    while True:
        schedule.run_pending()
        time.sleep(60)
