#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-11 8:55
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : tools.py
# @Software: PyCharm

import os
from datetime import datetime

import MySQLdb
import yaml


def init_fold():
    fold = 'file'
    if not os.path.exists(fold):
        os.mkdir(fold)


def get_connect_cursor():
    # 读入配置文件
    config = init()
    sql_config = config['sql']
    # 打开数据库连接
    connect = MySQLdb.connect('localhost', sql_config['username'], sql_config['password'], sql_config['name'],
                              charset='utf8', autocommit=1)
    return connect


def get_msg_id(conn):
    """
    根据数据库已有数据
    判断 msg 在当天的 id
    已保证当天内的 id 自增
    :param c:
    :return:
    """
    c = conn.cursor()
    c.execute('select message_num, create_time from msg_receive_message order by create_time desc limit 0, 1;')
    last_row = c.fetchall()  # ((2, datetime.datetime(2023, 8, 14, 15, 53, 28)),)
    c.close()
    if last_row is None:
        return 0

    last_row_datetime = last_row[0][1]
    if (datetime.now() - last_row_datetime).days > 0:
        return 0
    else:
        return last_row[0][0]


def init():
    """
    初始化
    :return:
    """
    # 配置文件

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sendMessageToGroup.yaml'),
              encoding='utf-8') as yaml_file:
        config = yaml.load(yaml_file, yaml.FullLoader)
    # todo：帮助问题
    # with open(config['help_msg_file'], encoding='utf-8', mode='r') as help_msg_file:
    #     config['help_msg'] = help_msg_file.read()

    return config


if __name__ == '__main__':
    conn, c = get_connect_cursor()
    print(get_msg_id(c))
