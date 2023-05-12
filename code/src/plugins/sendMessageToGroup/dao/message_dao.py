#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-11 17:20
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : message_dao.py
# @Software: PyCharm
from datetime import datetime
from sqlite3 import Cursor
from nonebot import logger


def save(c: Cursor, **kwargs):
    logger.info(f'保存消息：{kwargs}')
    sql = """
    insert into message (id, message_num, message_id_qq, qq_num, message_type, 
                         content, file_root, is_anonymous, create_time)
    values (?,?,?,?,?,?,?,?,?);
    """
    c.execute(sql, (kwargs['id'], kwargs['message_num'], kwargs['message_id_qq'], kwargs['qq_num'],
                    kwargs['message_type'], kwargs['content'], kwargs['file_root'], kwargs['is_anonymous'],
                    datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))


def get_qq_num_by_msg_num(c, message_num) -> int:
    sql = """
    select qq_num from message where message_num = ?;
    """
    return c.execute(sql, (message_num, )).fetchone()[0]
