from time import sleep, time, strftime, localtime

import pymongo

from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram.errors import ChatAdminRequired, MessageDeleteForbidden, UserAdminInvalid
from pyrogram import Client, filters

from others.operational_database import update_data, find_data


@Client.on_message(filters.incoming & filters.command(['check_in', 'check_in@{bot_name}'.format(bot_name=BOT_NAME)]))
def user_check_in(client, message):
    now_time = time()
    if message.from_user is None:
        reply_message = message.reply_text("❗**查询不到用户信息**")
        try:
            sleep(5)
            message.delete()
            reply_message.delete()
        except (ChatAdminRequired, MessageDeleteForbidden, UserAdminInvalid):
            reply_message.edit("❗**无删除用户信息权限，请授予管理权限**")
    else:
        filter_find = {
            "ID": message.from_user.id
        }
        if find_data(AllGroupMemberDatabaseName, message.chat.id, filter_find)['Last_check_in_data'] is None:
            update_group_member = {
                "$set": {
                    "Last_check_in_data": now_time
                }
            }
            update_filter = {
                "ID": message.from_user.id
            }
            update_data(AllGroupMemberDatabaseName, message.chat.id, update_group_member, update_filter)
            reply_message = message.reply_text("签到成功")
        else:
            reply_message = message.reply_text("❗**您今天已经签过到了**")
        try:
            sleep(5)
            message.delete()
            reply_message.delete()
        except (ChatAdminRequired, MessageDeleteForbidden, UserAdminInvalid, UnboundLocalError):
            reply_message.edit("❗**无删除用户信息权限，请授予管理权限**")
