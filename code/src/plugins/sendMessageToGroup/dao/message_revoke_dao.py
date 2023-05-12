#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-12 14:31
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : message_revoke_dao.py
# @Software: PyCharm

from datetime import datetime
from sqlite3 import Cursor


def save(c: Cursor, data):
    sql = """
    insert into message_revoke (id, message_id, create_time) 
    VALUES (?,?,?)
    """
    c.execute(sql, data + [datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')])
