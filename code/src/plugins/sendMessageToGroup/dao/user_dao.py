#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-11 17:20
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : user_dao.py
# @Software: PyCharm
import re
from datetime import datetime
from sqlite3 import Cursor

from nonebot import logger


def select_by_qq_num(c: Cursor, qq_num: int) -> tuple|None:
    """
    根据 qq_num 查询用户数据
    老用户返回信息
    新用户返回 None
    :param c:
    :param qq_num:
    :return:
    """
    logger.info(f'用户信息查询：{qq_num}')
    sql = """
    select id, qq_num, nickname, is_anonymous, create_time, update_time from 
    user where qq_num == ?;
    """

    user_info = c.execute(sql, (qq_num, )).fetchone()
    return user_info


def save(c: Cursor, guid: int, qq_num: int):
    """
    保存新用户信息
    :param guid:
    :param c:
    :param qq_num:
    :return: None
    """
    logger.info(f'用户信息保存：{qq_num}')
    sql = """
    insert into user (id, qq_num, nickname, is_anonymous, create_time, update_time)
    values (?,?,?,?,?,?);
    """
    c.execute(sql, (guid, qq_num, None, 0,
                    datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                    datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))


def change_nickname(c: Cursor, qq_num, msg):
    nickname = re.sub(r'昵称：', '', msg)
    logger.info(f'用户 {qq_num} 修改昵称为 {nickname}')
    sql = """
        UPDATE user set nickname=?, update_time=? where qq_num=?;
    """
    c.execute(sql, (nickname, datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), qq_num))
    return nickname
