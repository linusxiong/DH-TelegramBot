from datetime import datetime
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import update_data_one, find_data, check_database, check_table
from others.package import check_delete_message_right


@Client.on_message(filters.incoming & ~filters.private & filters.command(['check_in', f'check_in@{BOT_NAME}']))
def user_check_in(client, message):
    now_time = datetime.timestamp(datetime.now())
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
            last_check_in_data = find_data(AllGroupMemberDatabaseName, message.chat.id, filter_find)[
                'Last_check_in_data']
            # 从未签过到
            if last_check_in_data is None:
                update_group_member = {
                    "$set": {
                        "Last_check_in_data": now_time
                    }
                }
                update_filter = {
                    "ID": message.from_user.id
                }
                update_data_one(AllGroupMemberDatabaseName, message.chat.id, update_group_member, update_filter)
                reply_message = message.reply_text(
                    f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})签到成功"
                )
            # 已有签到数据
            if last_check_in_data is not None:
                now = datetime.fromtimestamp(now_time)
                last = datetime.fromtimestamp(last_check_in_data)
                days = (now - last).days
                # 如果现在时间和签到时间相差大于或等于1则表明当天未签到
                if days >= 1:
                    update_group_member = {
                        "$set": {
                            "Last_check_in_data": now_time
                        }
                    }
                    update_filter = {
                        "ID": message.from_user.id
                    }
                    update_data_one(AllGroupMemberDatabaseName, message.chat.id, update_group_member, update_filter)
                    reply_message = message.reply_text(
                        f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})签到成功，上一次签到在{days}天前"
                    )

                    # 如果现在时间和签到时间未大于一天则重复签到
                elif days == 0:
                    reply_message = message.reply_text("**您今天已经签过到了**")
            check_delete_message_right(message, reply_message, send_message=None)
