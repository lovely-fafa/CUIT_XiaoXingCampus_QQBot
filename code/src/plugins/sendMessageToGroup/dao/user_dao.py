#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-05-11 17:20
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : user_dao.py
# @Software: PyCharm

from datetime import datetime
from typing import Any, Union

from nonebot import logger


def select_by_qq_num(conn, qq_num: int) -> list[Any]:
    """
    根据 qq_num 查询用户数据
    老用户返回信息
    新用户返回 None
    :param c:
    :param qq_num:
    :return:
    """
    c = conn.cursor()
    logger.debug(f'查询用户信息 | qq_num={qq_num}')
    c.execute('select nickname from msg_user where qq_num = %s', (qq_num,))
    data = c.fetchall()
    c.close()
    return data


def save(conn, qq_num: int, nickname: Union[str | None]):
    """
    保存新用户信息
    :param nickname:
    :param c:
    :param qq_num:
    :return: None
    """
    c = conn.cursor()
    logger.debug(f'保存用户信息 |qq_num={qq_num} nickname={nickname}')
    c.execute('insert into msg_user (qq_num, nickname, create_time, update_time) values (%s, %s, %s, %s)',
              (qq_num, nickname, datetime.now(), datetime.now()))
    c.close()
    conn.commit()


def change_nickname(conn, qq_num, nickname):
    c = conn.cursor()
    c.execute('UPDATE msg_user set nickname=%s, update_time=%s where qq_num=%s',
              (nickname, datetime.now(), qq_num))
    conn.commit()
    c.close()


def get_blacklist(conn):
    c = conn.cursor()
    c.execute('select qq_num from management_blacklist where status = 1')
    blacklist = c.fetchall()
    c.close()
    if blacklist:
        black = [i[0] for i in blacklist]
        logger.info(f'查询黑名单 | blacklist={black}')
        return black
    else:
        logger.info(f'查询黑名单 | blacklist=[]')
        return []


if __name__ == '__main__':
    import MySQLdb

    connect = MySQLdb.connect('localhost', 'root', '555555s', 'xiaoxing_bot',
                              charset='utf8')

    # 使用cursor()方法获取操作游标
    c = connect.cursor()
    # save(c, 125, '123')
    print(select_by_qq_num(c, 123))
