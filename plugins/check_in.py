from time import time
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import update_data_one, find_data, check_database, check_table
from others.package import check_delete_message_right


@Client.on_message(filters.incoming & filters.command(['check_in', 'check_in@{bot_name}'.format(bot_name=BOT_NAME)]))
def user_check_in(client, message):
    now_time = time()
    # 防止匿名签到，因为读不到信息
    if message.from_user is None:
        reply_message = message.reply_text("❗**查询不到用户信息**")
        check_delete_message_right(message, reply_message, send_message=None)
    else:
        filter_find = {
            "ID": message.from_user.id
        }
        if check_table(message.chat.id, AllGroupMemberDatabaseName) is True:
            message.reply_text("❗**请先进行```/init```初始化操作**")
        else:
            # 如果'Last_check_in_data'字段为空则没签过到
            if find_data(AllGroupMemberDatabaseName, message.chat.id, filter_find)['Last_check_in_data'] is None:
                update_group_member = {
                    "$set": {
                        "Last_check_in_data": now_time
                    }
                }
                update_filter = {
                    "ID": message.from_user.id
                }
                update_data_one(AllGroupMemberDatabaseName, message.chat.id, update_group_member, update_filter)
                reply_message = message.reply_text("签到成功_试运行")
            else:
                reply_message = message.reply_text("**您今天已经签过到了**")
            check_delete_message_right(message, reply_message, send_message=None)
