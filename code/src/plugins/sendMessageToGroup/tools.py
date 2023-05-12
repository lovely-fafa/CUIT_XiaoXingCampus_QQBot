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
from sqlite3 import Cursor

import yaml


def init_sqlite(sql):
    """
    创建数据库
    创建数据库表
    :param sql: 数据库路径
    :return:
    """
    import sqlite3

    conn = sqlite3.connect(sql)
    c = conn.cursor()
    c.execute('''
            create table user
            (
                id           INTEGER primary key not null,
                qq_num       TEXT                not null,
                nickname     TEXT,
                is_anonymous INT                 not null
            );''')
    c.execute('''
            create table message
            (
                id           INTEGER primary key not null,
                msg_id       int                 NOT NULL,
                message_id   INTEGER             not null,
                content      Text,
                qq_num       TEXT                not null,
                msg_type     int                 not null,
                file_root    text,
                is_anonymous INT                 not null
            )''')
    conn.commit()
    conn.close()


def get_msg_id(c):
    """
    根据数据库已有数据
    判断 msg 在当天的 id
    已保证当天内的 id 自增
    :param c:
    :return:
    """
    cursor: Cursor = c.execute('select message_num, create_time from message msg_id;')
    last_row = None
    for i in cursor:
        last_row = i

    if last_row is None:
        return 0
    msg_date = datetime.strptime(last_row[1], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - msg_date).days > 0:
        return 0
    else:
        return last_row[0]


def init():
    """
    初始化
    :return:
    """
    # 配置文件

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sendMessageToGroup.yaml'),
              encoding='utf-8') as yaml_file:
        config = yaml.load(yaml_file, yaml.FullLoader)

    with open(config['help_msg_file'], encoding='utf-8', mode='r') as help_msg_file:
        config['help_msg'] = help_msg_file.read()

    # 数据库初始化
    sqlite3_file = config['sqlite3_file']
    if not os.path.exists(sqlite3_file):
        init_sqlite(sqlite3_file)

    return config






if __name__ == '__main__':
    print(init())
