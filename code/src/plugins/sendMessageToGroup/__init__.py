#!/usr/bin/python 3.10
# -*- coding: utf-8 -*- 
#
# @Time    : 2022-09-25 18:25
# @Author  : 发发
# @QQ      : 1315337973
# @File    : sendMessageToGroup.py
# @Software: PyCharm

# 可参考插件商店的 nonebot_plugin_forwarder 转发姬插件
from time import localtime, sleep
from random import random
from datetime import datetime

from nonebot import logger
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent
import asyncio

from . import config

initial_day = datetime.now().day
initial_id = 0
msg_matcher = on_message(priority=10, block=False)


async def send_msg_to_group(bot: Bot, group_id: str, msg: str, from_id: str, msg_id: str, from_nickName: str):
    msg_send = f'{msg_id}.{msg}\n来源：{from_nickName}【{from_id}】'
    logger.debug(f'消息转发至：{group_id}')
    await bot.send_group_msg(group_id=int(group_id),
                             message=msg_send,
                             auto_escape=False)


@msg_matcher.handle()
async def _(bot: Bot, event: PrivateMessageEvent):

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
        await send_msg_to_group(bot=bot,
                                group_id=gid,
                                msg=msg,
                                from_id=from_id,
                                msg_id=str(initial_id),
                                from_nickName=nickName)
        sleep(random())
    # tasks = [send_msg_to_group(bot=bot,
    #                            group_id=gid,
    #                            msg=msg,
    #                            from_id=from_id,
    #                            msg_id=str(initial_id)) for gid in config.forwarder_destination_group]
    # await asyncio.wait(tasks)







