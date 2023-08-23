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

import requests
from nonebot import logger
from nonebot import on_message, on_notice, on_regex
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, FriendRecallNoticeEvent, Event, NoticeEvent, Message
from nonebot_plugin_apscheduler import scheduler

from .dao.target_group_dao import get_target_group_num
from .tools import init, get_msg_id, get_connect_cursor, init_fold
from .dao import user_dao, message_dao, message_group_dao, message_revoke_dao

logger.info('初始化 转发 插件')
logger.info('连接数据库...')
conn = get_connect_cursor()
logger.info('连接数据库成功')

# 初始化
logger.info('获取消息序号...')
message_num = get_msg_id(conn)
logger.info('获取消息序号成功')

logger.info('创建依赖文件夹...')
init_fold()
logger.info('创建依赖文件夹成功')


# 定时器
@scheduler.scheduled_job("cron", hour="23", minute="59", second="59")
def run_every_day():
    global message_num
    message_num = 0


help_msg_matcher = on_regex(r'^帮助$', priority=5, block=True)
change_nickname = on_regex(r'^昵称：(.*?)', priority=5, block=True)
send_msg_matcher = on_message(priority=10, block=False)  # 优先级数字越小越先响应
file_msg_matcher = on_notice(priority=16, block=True)
revoke_msg_matcher = on_notice(priority=1, block=False)  # tmd 这个地方 撤回是 notice 事件 怎么会是 on_message 啊

logger.info('成功载入 转发 插件')


@help_msg_matcher.handle()
async def _():
    await help_msg_matcher.finish(Message('帮助'))  # todo: 帮助问题


@change_nickname.handle()
async def change_nickname_fun(event: Event):
    qq_num = event.user_id
    nickname = re.sub(r'昵称：', '', str(event.message))
    logger.info(f'更改昵称 |  qq_num={qq_num} nickname={nickname}')

    user_dao.change_nickname(conn, qq_num, nickname)
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

    qq_num = event.user_id
    if qq_num in user_dao.get_blacklist(conn):
        return
    msg = str(event.message)

    # 查询用户数据
    user_info = user_dao.select_by_qq_num(conn, qq_num)  # (('123',),)
    if not user_info:
        nickname = event.sender.nickname
        user_dao.save(conn, qq_num, nickname)
    else:
        nickname = event.sender.nickname if not user_info else user_info[0][0]

    # 保存消息
    logger.info(f'预转发消息 | msg_num={message_num} qq_num={qq_num} msg={msg}')
    message_save = {
        'message_num': message_num,
        'tencent_id': event.message_id,
        'user_qq_num': qq_num,
        'message_type': 1,
        'content': msg,
        'file_root': None,
    }
    message_id = message_dao.save(conn, **message_save)

    # 准备转发
    msg_send = f'{message_num}.{msg}\n提交来源：{nickname}\n提交QQ：{qq_num}'

    # 是否有 艾特
    for aite_num in re.findall(r'艾特(\d+)', msg):
        qq_num = message_dao.get_qq_num_by_msg_num(conn, int(aite_num))
        msg_send = re.sub(rf'艾特{aite_num}', f'[CQ:at,qq={qq_num}] ', msg_send)

    message_dict = {k: msg_send for k in get_target_group_num(conn)}

    # 是否有 回复
    if search := re.search(r'^回(\d+)\D', msg):
        reply_msg_id = search.group(1)
        msg_ids_bot = message_group_dao.get_group_msg_id_group_id_by_message_num(conn, int(reply_msg_id))
        for group_num, tencent_id in msg_ids_bot:
            message_dict[group_num] = f'[CQ:reply,id={tencent_id}] {msg_send}'

    message_group_save = []
    for group_num, msg in message_dict.items():

        try:
            send_group_msg_result = await bot.send_group_msg(group_id=group_num,
                                                             message=msg,
                                                             auto_escape=False)
            logger.debug(f'消息转发成功 | group_num={group_num}  msg_num={message_num}')
            message_group_save.append([
                message_id,
                group_num,
                send_group_msg_result['message_id'],
                1
            ])
        except Exception as e:
            logger.warning(f'消息转发失败 | group_num={group_num}  msg_num={message_num} e={e}')
            message_group_save.append([
                message_id,
                group_num,
                None,
                0
            ])
        sleep(random())
    message_group_dao.save(conn, message_group_save)


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

        qq_num = notice.user_id
        if qq_num in user_dao.get_blacklist(conn):
            return
        file_name = notice.file['name']

        # 查询用户数据
        user_info = user_dao.select_by_qq_num(conn, qq_num)  # (('123',),)
        if user_info is None:
            user_dao.save(conn, qq_num, None)

        message_save = {
            'message_num': message_num,
            'tencent_id': None,
            'user_qq_num': qq_num,
            'message_type': 2,
            'content': None,
            'file_root': file_name,
        }
        message_dao.save(conn, **message_save)
        logger.info(f'发送文件 | qq_num={qq_num} filename={file_name}')

        send_file_name = f'_by_{qq_num}.'.join(file_name.rsplit('.', 1))

        file_url = notice.file['url']
        resp = requests.get(file_url)
        with open(f'./file/{send_file_name}', mode='wb') as f:
            f.write(resp.content)

        # 接下来直接调用的 go-cqhttp 的接口 具体在 README.md 里面有讲
        for gid in get_target_group_num(conn):
            await bot.call_api('upload_group_file',
                               group_id=gid,
                               file=f'{os.path.abspath(f"./file/{send_file_name}")}',
                               name=send_file_name)


@revoke_msg_matcher.handle()
async def matching_revoke_msg(bot: Bot, event: FriendRecallNoticeEvent):
    """
    消息撤回函数
    :param bot:
    :param event:
    :return:
    """
    qq_num = event.user_id
    tencent_id = event.message_id
    logger.info(f'消息撤回 | qq_num={qq_num} msg_id={tencent_id}')

    tencent_ids = message_group_dao.get_group_tencent_id_by_user_tencent_id(conn, tencent_id)

    for tencent_id in tencent_ids:
        await bot.delete_msg(message_id=tencent_id)

    message_revoke_dao.save(conn, tencent_id)
