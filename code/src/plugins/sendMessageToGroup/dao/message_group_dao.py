#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-12 11:53
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : message_group_dao.py
# @Software: PyCharm

from datetime import datetime
from sqlite3 import Cursor


def save(c: Cursor, data: list[list]):
    """
    保存 Bot 发送到群里面的消息
    :param c:
    :param data:
    :return:
    """
    sql = """
    insert into message_group (id, message_id, group_id, message_id_qq, create_time) 
    VALUES (?,?,?,?,?)
    """
    c.executemany(sql,
                  [i + [datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')] for i in data])


def get_group_msg_id_group_id_by_message_num(c: Cursor, message_num: int):
    """

    :param message_num:
    :param c:
    :return:
    """
    sql = """
        select group_id, message_id_qq
        from message_group
        where message_id = (select id from message where message_num = ?);
    """
    return c.execute(sql, (message_num, )).fetchall()


def get_group_msg_id_by_user_msg_id(c, msg_id):
    """

    :param c:
    :param msg_id:
    :return:
    """
    sql = """
        select message_group.message_id_qq
        from message_group
        where message_id = (select id from message where message.message_id_qq = ?);
    """
    return c.execute(sql, (msg_id, )).fetchall()
