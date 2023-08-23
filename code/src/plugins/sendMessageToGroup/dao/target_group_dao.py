#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2023-08-14 20:45
# @Author  : 发发
# @QQ      : 1315337973
# @GitHub  : https://github.com/lovely-fafa
# @File    : target_group_dao.py
# @Software: PyCharm

from typing import List

from nonebot import logger


def get_target_group_id_by_num(conn, num):
    c = conn.cursor()
    c.execute('select id from management_target_group where group_num = %s', (num, ))
    data = c.fetchall()[0][0]
    c.close()
    return data


def get_target_group_num(conn) -> List[int]:
    c = conn.cursor()
    c.execute('select group_num from management_target_group where status = 1')
    target_group = c.fetchall()
    c.close()

    if target_group is None:
        logger.warning('查询目标群为空')
        return []
    target = [i[0] for i in target_group]
    logger.info(f'查询目标群 | target={target}')
    return target


if __name__ == '__main__':
    import MySQLdb

    connect = MySQLdb.connect('localhost', 'root', '555555s', 'xiaoxing_bot',
                              charset='utf8')
    c = connect.cursor()

    print(get_target_group_id_by_num(c, 227462320))


