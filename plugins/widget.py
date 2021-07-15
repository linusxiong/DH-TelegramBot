from pyrogram import Client, filters
from others.package import check_delete_message_right
from config import BOT_NAME


# 存活性测试
@Client.on_message(filters.incoming & filters.command(['ping', 'ping@{bot_name}'.format(bot_name=BOT_NAME)]))
def ping(message):
    send_message = message.reply_text("🏓️")
    check_delete_message_right(message, None, send_message)


# 查询用户ID
@Client.on_message(filters.incoming & filters.command(['queryid', 'queryid@{bot_name}'.format(bot_name=BOT_NAME)]))
def query_id(message):
    if message.from_user is None:
        message.reply_text("❗**查询不到用户信息**")
    else:
        if message.from_user.language_code == "zh-hans":
            reply_message = message.reply_text("你的用户ID为：" + str(message.from_user.id))
        else:
            reply_message = message.reply_text("Your User ID is:" + str(message.from_user.id))
        check_delete_message_right(message, reply_message, send_message=None)


# 查询用户数据中心
@Client.on_message(filters.incoming & filters.command(['dc', 'dc@{bot_name}'.format(bot_name=BOT_NAME)]))
def query_user_id(message):
    if message.from_user is None:
        message.reply_text("❗**查询不到用户信息**")
    else:
        if message.from_user.language_code == "zh-hans":
            reply_message = message.reply_text(
                "[{}](tg://user?id={})的数据中心为：**DC{}**".format(message.from_user.username, message.from_user.id,
                                                              str(message.from_user.dc_id)))
        else:
            reply_message = message.reply_text(
                "Your Account Datacenter is: **DC{}**".format(str(message.from_user.dc_id)))
        check_delete_message_right(message, reply_message, send_message=None)
