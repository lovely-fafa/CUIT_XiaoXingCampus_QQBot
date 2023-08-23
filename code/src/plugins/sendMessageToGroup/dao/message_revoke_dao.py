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


def save(conn, tencent_id):
    c = conn.cursor()
    sql = """
    insert into msg_revoke (message_id, create_time, update_time) 
    VALUES ((select id from msg_receive_message where tencent_id = %s),%s,%s)
    """
    c.execute(sql, (tencent_id, datetime.now(), datetime.now()))
    c.close()
    conn.commit()
