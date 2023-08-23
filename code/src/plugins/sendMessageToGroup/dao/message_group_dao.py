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

from . import target_group_dao


def save(conn, data: list[list]):
    """
    保存 Bot 发送到群里面的消息
    :param c:
    :param data:
    :return:
    """
    c = conn.cursor()
    sql = """
    insert into msg_send_message (message_id, target_group_id, tencent_id, status, create_time, update_time)
    value (%s, %s, %s, %s, %s, %s)
    """
    now = datetime.now()

    for item in data:
        item[1] = target_group_dao.get_target_group_id_by_num(conn, item[1])
        item.extend([now] * 2)

    c.executemany(sql, data)
    c.close()
    conn.commit()


def get_group_msg_id_group_id_by_message_num(conn, message_id: int):
    """

    :param message_id:
    :param c:
    :return:
    """
    c = conn.cursor()
    sql = """
        select group_num, s.tencent_id
        from msg_send_message as s
        left join msg_receive_message as r on s.message_id = r.id
        left join management_target_group on target_group_id = management_target_group.id
        where message_num = %s
        and r.create_time = (select create_time from msg_receive_message where message_num = %s order by create_time desc limit 1)
    """
    c.execute(sql, (message_id, message_id))
    data = c.fetchall()
    c.close()
    return data


def get_group_tencent_id_by_user_tencent_id(conn, msg_id):
    """

    :param c:
    :param msg_id:
    :return:
    """
    c = conn.cursor()
    sql = """
        select msg_send_message.tencent_id from msg_send_message
        left join msg_receive_message on message_id = msg_receive_message.id 
        where msg_receive_message.tencent_id = %s
    """
    c.execute(sql, (msg_id,))
    data = [i[0] for i in c.fetchall()]
    c.close()
    return data
