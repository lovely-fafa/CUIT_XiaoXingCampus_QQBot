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
from nonebot import logger


def save(conn, **kwargs):
    c = conn.cursor()
    logger.debug(f'保存消息 | msg={kwargs}')
    sql = """
    insert into msg_receive_message (message_num, tencent_id, user_qq_num, message_type, content, file_root, create_time, update_time)
    values (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    c.execute(sql, (kwargs['message_num'], kwargs['tencent_id'], kwargs['user_qq_num'],
                    kwargs['message_type'], kwargs['content'], kwargs['file_root'],
                    datetime.now(), datetime.now()))
    last_id = c.lastrowid
    c.close()
    conn.commit()
    return last_id


def get_qq_num_by_msg_num(conn, message_num) -> int:
    """
    根据消息编号 返回发消息人的 QQ号 用于艾特功能
    :param c:
    :param message_num:
    :return:
    """
    c = conn.cursor()
    c.execute('select user_qq_num from msg_receive_message where message_num = %s order by create_time desc limit 1',
              (message_num, ))
    data = c.fetchall()[0][0]
    c.close()
    return data
