#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-09-25 18:25
# @Author  : 发发
# @QQ      : 1315337973
# @File    : sendMessageToGroup.py
# @Software: PyCharm
import os
# 可参考插件商店的 nonebot_plugin_forwarder 转发姬插件
from time import localtime, sleep
from random import random
from datetime import datetime
from io import BytesIO

import requests
from nonebot import logger
from nonebot import on_message, on_notice, on_regex
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, FriendRecallNoticeEvent, Event, NoticeEvent, Message


from . import config

initial_day = datetime.now().day
initial_id = 0

msg_dict = {}  # 显然这个地方是很笨的方法 我们应该存数据库 但是我不会

help_msg_matcher = on_regex(r'^帮助$', priority=5, block=True)


@help_msg_matcher.handle()
async def _():
    await help_msg_matcher.finish(Message(config.help_msg))


send_msg_matcher = on_message(priority=10, block=False)  # 优先级数字越小越先响应


@send_msg_matcher.handle()
async def matching_send_msg(bot: Bot, event: PrivateMessageEvent):
    """
    匹配私聊消息 并转发
    :param bot:
    :param event:
    :return:
    """

    global initial_day
    global initial_id
    msg_time_day = localtime(event.time)[2]
    # 当天的
    if msg_time_day == initial_day:
        initial_id += 1

    # 新的一天
    else:
        initial_day = msg_time_day
        initial_id = 1

    from_id = str(event.user_id)
    msg = str(event.message)
    nickName = event.sender.nickname

    logger.debug(f'预转发消息：{msg} | 来源：{from_id}')

    for gid in config.forwarder_destination_group:

        msg_send = f'{initial_id}.{msg}\n提交来源：{nickName}\n提交QQ：{from_id}'
        logger.debug(f'消息转发至：{gid}')
        await bot.send_group_msg(group_id=int(gid),
                                 message=msg_send,
                                 auto_escape=False)
        sleep(random())


file_msg_matcher = on_notice(priority=16, block=True)


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
        print(dir(notice.get_user_id))
        file_name = f'_by_{notice.user_id}.'.join(notice.file['name'].rsplit('.', 1))
        file_url = notice.file['url']

        resp = requests.get(file_url)
        with open(f'./data/sendMessageToGroup/file/{file_name}', mode='wb') as f:
            f.write(resp.content)

        # 接下来直接调用的 go-cqhttp 的接口 具体在 README.md 里面有讲
        for gid in config.forwarder_destination_group:
            await bot.call_api('upload_group_file',
                               group_id=gid,
                               file=f'{os.path.abspath(f"./data/sendMessageToGroup/file/{file_name}")}',
                               name=file_name)


# recall_msg_matcher = on_notice(priority=1, block=False)  # tmd 这个地方 撤回是 notice 事件 怎么会是 on_message 啊
# @recall_msg_matcher.handle()
# async def matching_recall_msg(bot: Bot, event: FriendRecallNoticeEvent):
#     """
#     消息撤回函数
#     :param bot:
#     :param event:
#     :return:
#     """
#
#     msg_id = event.message_id
#
#     print(msg_id)
#     sleep(1)
#     await bot.delete_msg(message_id=msg_id)






