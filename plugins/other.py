from time import sleep
from pyrogram import Client, filters
from config import BOT_NAME


# @Client.on_raw_update()
# def raw(client, update, users, chats):
#     print(chats)

# 存活性测试
@Client.on_message(filters.incoming & filters.command(['ping', 'ping@{bot_name}'.format(bot_name=BOT_NAME)]))
def ping(client, message):
    send_message = message.reply_text("🏓️")
    sleep(5)
    send_message.delete()
    message.delete()


# 查询用户ID
@Client.on_message(filters.incoming & filters.command(['queryid', 'queryid@{bot_name}'.format(bot_name=BOT_NAME)]))
def query_id(client, message):
    if message.from_user.language_code == "zh-hans":
        reply_message = message.reply_text("你的用户ID为：" + str(message.from_user.id))
    else:
        reply_message = message.reply_test("Your User ID is:" + str(message.from_user.id))

    sleep(5)
    reply_message.delete()
    message.delete()


# 查询用户数据中心
@Client.on_message(filters.incoming & filters.command(['dc', 'dc@{bot_name}'.format(bot_name=BOT_NAME)]))
def query_user_id(client, message):
    if message.from_user.language_code == "zh-hans":
        reply_message = message.reply_text(
            "[{}](tg://user?id={})的数据中心为：**DC{}**".format(message.from_user.username, message.from_user.id,
                                                          str(message.from_user.dc_id)))
    else:
        reply_message = message.reply_text("Your Account Datacenter is: **DC{}**".format(str(message.from_user.dc_id)))

    sleep(5)
    reply_message.delete()
    message.delete()
