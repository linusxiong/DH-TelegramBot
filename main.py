import random
import time
from pyrogram import Client, filters
import telebot
from datetime import datetime, timedelta

# import database
from config import TOKEN, BanMeReplayAddress, api_id, api_hash

# from tg_client.client import get_all_group_member


bot = telebot.TeleBot(TOKEN, parse_mode=None)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "欢迎使用本Telegram Bot")


@bot.message_handler(commands=['checkin'])
def check_in(message):
    if message.chat.type == "group" or "supergroup":
        bot.reply_to(message, "签到成功-测试中")
    else:
        if message.chat.type == "private":
            bot.reply_to(message, "签到成功-测试中")


@bot.message_handler(commands=['banme'])
def ban_me(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "你私聊我我怎么Ban你啊淦,有本事去群里对线！！")

    elif message.chat.type == "group" or "supergroup":
        block_time = time.time() + random.randint(100, 500)
        if bot.get_chat_member(message.chat.id, message.from_user.id).status == "member" or "restricted":
            bot.reply_to(message, "恭喜您获得" + str(block_time) + "秒禁言时间")
            bot.reply_to(message, str(block_time))
            bot.restrict_chat_member(message.chat.id, message.from_user.id, block_time, can_send_messages=False,
                                     can_send_polls=False, can_send_other_messages=False, can_send_media_messages=False)
        else:
            bot.send_photo(message.chat.id, photo=BanMeReplayAddress, reply_to_message_id=message.chat.id)


# 查询用户个人ID
@bot.message_handler(commands=['queryid'])
def query_user_id(message):
    if message.from_user.language_code == "zh-hans":
        bot.reply_to(message, "你的用户ID为：" + str(message.from_user.id))
    else:
        bot.reply_to(message, "Your User ID is:" + str(message.from_user.id))


@bot.message_handler(commands=['test'])
def test(message):
    replay = str(bot.get_chat_member(message.chat.id, message.from_user.id).status)
    bot.reply_to(message, get_all_group_member(message.chat.id))


#     # get_chat_members_count获取chat_id的群组人数, 从bot接受到的信息的message查询群组chat_id
#     # print(client.get_all_group_member(message.chat.id, bot.get_chat_members_count(message.chat.id)))
#     # print(type(message.chat.id))
#     # print(f"{bot.get_chat_members_count(message.chat.id)}")
#     # print(f"{client.get_all_group_member(message.chat.id, bot.get_chat_members_count(message.chat.id))}")
#
#     # loop = asyncio.get_
#     # print(client.get_all_group_member(-1001426942183, 11))
#     # result = get_all_group_member(message.chat.id, bot.get_chat_members_count(message.chat.id))
#     count = bot.get_chat_members_count(message.chat.id)
#     result = str(get_all_group_member(message.chat.id, count))
#     bot.reply_to(message, result)
#     # bot.reply_to(message, client.get_all_group_member(-1001426942183, 11))
#     # bot.reply_to(message, str(bot.get_chat_members_count(message.chat.id)))
#
#
# @bot.message_handler(commands=['test'])
# def test(messages):
#     for m in messages:
#         count = bot.get_chat_members_count(m.chat.id)
#         result = str(get_all_group_member(m.chat.id, count))
#         bot.reply_to(m, result)
#
#
# bot.set_update_listener(test)

with Client("my_account", api_id, api_hash) as app:
    def get_all_group_member(chat_id):
        list = []
        for member in app.iter_chat_members(chat_id):
            list.append(member.user.id)
            print(member.user.id)


bot.polling()
