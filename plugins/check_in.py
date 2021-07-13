from time import sleep, time, strftime, localtime
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram.errors import ChatAdminRequired, MessageDeleteForbidden, UserAdminInvalid
from pyrogram import Client, filters


@Client.on_message(filters.incoming & filters.command(['check_in', 'check_in@{bot_name}'.format(bot_name=BOT_NAME)]))
def user_check_in(client, message):
    try:
        reply_message = message.reply_text("签到成功")
        now_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print(message)
        sleep(5)
        message.delete()
        reply_message.delete()
    except (ChatAdminRequired, MessageDeleteForbidden, UserAdminInvalid):
        reply_message.edit("❗**无删除用户信息权限，请授予管理权限**")
