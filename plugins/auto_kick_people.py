from time import time, sleep
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid

from config import BOT_NAME


@Client.on_message(filters.incoming & ~filters.private & filters.command(['auto_kick', 'auto_kick@{bot_name}'.format(bot_name=BOT_NAME)]))
def auto_kick(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ('administrator', 'creator'):
        if len(message.command) > 1:
            input_str = message.command
            sent_message = message.reply_text("🚮**删除不活跃成员需要一定时间**")
            count = 0
            for member in client.iter_chat_members(message.chat.id):
                if member.user.status in input_str and not member.status in ('administrator', 'creator'):
                    try:
                        client.kick_chat_member(message.chat.id, member.user.id, int(time() + 45))
                        count += 1
                        sleep(1)
                    except (ChatAdminRequired, UserAdminInvalid):
                        sent_message.edit("❗**无管理权限，请授予管理权限**")
                        sleep(5)
                        # client.leave_chat(message.chat.id)
                        break
                    except FloodWait as e:
                        sleep(e.x)
            try:
                sent_message.edit("✔️ **成功踢出{} 成员.**".format(count))
            except ChatWriteForbidden:
                pass
        else:
            message.reply_text("❗**获取参数失败，请使用help命令查看可用参数**")
    else:
        sent_message = message.reply_text("❗ **操作者必须为管理员身份**")
        sleep(5)
        sent_message.delete()


@Client.on_message(filters.incoming & ~filters.private & filters.command(['kick_deleted', 'kick_deleted@{bot_name}'.format(bot_name=BOT_NAME)]))
def kick_deleted(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ('administrator', 'creator'):
        sent_message = message.reply_text("🚮**删除不活跃成员需要一定时间**")
        count = 0
        for member in client.iter_chat_members(message.chat.id):
            if member.user.is_deleted and not member.status in ('administrator', 'creator'):
                try:
                    client.kick_chat_member(message.chat.id, member.user.id, int(time() + 45))
                    count += 1
                    sleep(1)
                except (ChatAdminRequired, UserAdminInvalid):
                    sent_message.edit("❗**无管理权限，请授予管理权限**")
                    sleep(5)
                    # client.leave_chat(message.chat.id)
                    break
                except FloodWait as wait:
                    sleep(wait.x)
        try:
            sent_message.edit("✔️ **成功踢出{} 已删除账户**".format(count))
        except ChatWriteForbidden:
            pass
    else:
        sent_message = message.reply_text("❗ **操作者必须为管理员身份**")
        sleep(5)
        sent_message.delete()


@Client.on_message(filters.incoming & ~filters.private & filters.command(['group_status', 'group_status@{bot_name}'.format(bot_name=BOT_NAME)]))
def group_status(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in ('administrator', 'creator'):
        sent_message = message.reply_text("**信息查询中**")
        recently = 0
        within_week = 0
        within_month = 0
        long_time_ago = 0
        deleted_acc = 0
        uncached = 0
        bot = 0
        for member in client.iter_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.status == "recently":
                recently += 1
            elif user.status == "within_week":
                within_week += 1
            elif user.status == "within_month":
                within_month += 1
            elif user.status == "long_time_ago":
                long_time_ago += 1
            else:
                uncached += 1

        status_info = "**{}\n成员状态**\n\n```最近发言``` - {}\n```近一周发言人数``` - {}\n```近一月发言人数``` - {}\n```很久未上线人数``` - {" \
                      "}\n账户已删除人数 - {}\n机器人人数 - {}\n无数据 - {} "
        sent_message.edit(
            status_info.format(message.chat.title, recently, within_week, within_month, long_time_ago, deleted_acc,
                               bot, uncached))
