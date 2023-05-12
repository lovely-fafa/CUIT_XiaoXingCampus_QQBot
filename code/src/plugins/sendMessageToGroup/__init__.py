#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-09-25 18:25
# @Author  : 发发
# @QQ      : 1315337973
# @File    : sendMessageToGroup.py
# @Software: PyCharm

# 可参考插件商店的 nonebot_plugin_forwarder 转发姬插件
import os
import re
from time import sleep
from random import random
import sqlite3
import subprocess

import requests
import snowflake.client
from nonebot import logger
from nonebot import on_message, on_notice, on_regex
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, FriendRecallNoticeEvent, Event, NoticeEvent, Message
from nonebot_plugin_apscheduler import scheduler

from .tools import init, get_msg_id
from .dao import user_dao, message_dao, message_group_dao, message_revoke_dao

# 读入配置文件
config = init()
sqlite = config['sqlite3_file']
# 数据库连接
conn = sqlite3.connect(sqlite)
c = conn.cursor()

# 初始化
subprocess.Popen('snowflake_start_server')  # 雪花算法
message_num = get_msg_id(c)


# 定时器
@scheduler.scheduled_job("cron", hour="23", minute="59", second="59")
def run_every_day():
    global message_num
    message_num = 0


help_msg_matcher = on_regex(r'^帮助$', priority=5, block=True)
change_nickname = on_regex(r'^昵称：(.*?)', priority=5, block=True)
send_msg_matcher = on_message(priority=10, block=False)  # 优先级数字越小越先响应
file_msg_matcher = on_notice(priority=16, block=True)
recall_msg_matcher = on_notice(priority=1, block=False)  # tmd 这个地方 撤回是 notice 事件 怎么会是 on_message 啊


@help_msg_matcher.handle()
async def _():
    await help_msg_matcher.finish(Message(config['help_msg']))


@change_nickname.handle()
async def change_nickname_fun(event: Event):
    nickname = user_dao.change_nickname(c, event.user_id, str(event.message))
    conn.commit()
    await change_nickname.finish(f'昵称更改为：{nickname}')


@send_msg_matcher.handle()
async def matching_send_msg(bot: Bot, event: PrivateMessageEvent):
    """
    匹配私聊消息 并转发
    :param bot:
    :param event:
    :return:
    """
    global message_num
    message_num += 1

    from_id = event.user_id
    msg = str(event.message)

    # 查询用户数据
    user_info = user_dao.select_by_qq_num(c, from_id)
    if user_info is None:
        user_id = snowflake.client.get_guid()
        is_anonymous = 0
        nickname = event.sender.nickname
        user_dao.save(c, user_id, from_id)
        conn.commit()
    else:
        is_anonymous = user_info[3]
        nickname = event.sender.nickname if user_info[2] is None else user_info[2]

    # 保存消息
    logger.debug(f'预转发消息：{msg} | 来源：{from_id}')
    message_id = snowflake.client.get_guid()
    message_save = {
        'id': message_id,
        'message_num': message_num,
        'message_id_qq': event.message_id,
        'qq_num': from_id,
        'message_type': 1,
        'content': msg,
        'file_root': None,
        'is_anonymous': is_anonymous,
    }
    message_dao.save(c, **message_save)

    # 准备转发
    msg_send = f'{message_num}.{msg}\n提交来源：{nickname}\n提交QQ：{from_id}'
    msg_dict = {k: msg_send for k in config['forwarder_destination_group']}

    # 是否有 艾特
    if re.search(r'艾特(\d+)', msg):
        for aite_num in re.findall(r'艾特(\d+)', msg):
            qq_num = message_dao.get_qq_num_by_msg_num(c, int(aite_num))
            msg_send = re.sub(rf'艾特{aite_num}', f'[CQ:at,qq={qq_num}] ', msg_send)

    # 是否有 回复
    if re.search(r'^回(\d+)\D', msg):
        reply_msg_id = re.search(r'^回(\d+)\D', msg).group(1)
        msg_ids_bot = message_group_dao.get_group_msg_id_group_id_by_message_num(c, int(reply_msg_id))
        msg_send_clean = re.sub(r'^回\d+', '', msg_send)
        for group_num, msg_id_bot in msg_ids_bot:
            msg_dict[group_num] = f'[CQ:reply,id={msg_id_bot}] {msg_send_clean}'

    message_group_save = []
    for gid, msg in msg_dict.items():
        logger.debug(f'消息转发至：{gid}')
        send_group_msg_result = await bot.send_group_msg(group_id=int(gid),
                                                         message=msg,
                                                         auto_escape=False)
        message_group_save.append([
            snowflake.client.get_guid(),
            message_id,
            gid,
            send_group_msg_result['message_id']
        ])
        sleep(random())
    message_group_dao.save(c, message_group_save)
    conn.commit()


@file_msg_matcher.handle()
async def _(bot: Bot, notice: NoticeEvent):
    """
    群文件转发
    :param bot:
    :param notice:
    :return:
    """
    # 发送的是文件
    if notice.notice_type == 'offline_file':

        from_id = notice.user_id
        file_name = notice.file['name']

        # 查询用户数据
        user_info = user_dao.select_by_qq_num(c, from_id)
        if user_info is None:
            user_id = snowflake.client.get_guid()
            is_anonymous = 0
            user_dao.save(c, user_id, from_id)
            conn.commit()
        else:
            is_anonymous = user_info[3]

        message_id = snowflake.client.get_guid()
        message_save = {
            'id': message_id,
            'message_num': message_num,
            'message_id_qq': None,
            'qq_num': from_id,
            'message_type': 2,
            'content': None,
            'file_root': file_name,
            'is_anonymous': is_anonymous,
        }
        message_dao.save(c, **message_save)

        if is_anonymous:
            send_file_name = file_name
        else:
            send_file_name = f'_by_{from_id}.'.join(file_name.rsplit('.', 1))

        file_url = notice.file['url']
        resp = requests.get(file_url)
        with open(f'./data/sendMessageToGroup/file/{send_file_name}', mode='wb') as f:
            f.write(resp.content)

        # 接下来直接调用的 go-cqhttp 的接口 具体在 README.md 里面有讲
        for gid in config['forwarder_destination_group']:
            await bot.call_api('upload_group_file',
                               group_id=gid,
                               file=f'{os.path.abspath(f"./data/sendMessageToGroup/file/{send_file_name}")}',
                               name=file_name)


@recall_msg_matcher.handle()
async def matching_recall_msg(bot: Bot, event: FriendRecallNoticeEvent):
    """
    消息撤回函数
    :param bot:
    :param event:
    :return:
    """
    qq_num = event.user_id
    msg_id = event.message_id
    logger.info(f'用户：{qq_num} 撤回消息：{msg_id}')

    msg_ids_bot = message_group_dao.get_group_msg_id_by_user_msg_id(c, msg_id)

    for msg_id_bot in msg_ids_bot:
        logger.info(msg_id_bot)
        await bot.delete_msg(message_id=msg_id_bot[0])

    message_revoke_dao.save(c, [snowflake.client.get_guid(), msg_id])
    conn.commit()
