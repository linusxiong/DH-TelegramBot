import random
import telebot
import asyncio
from tg_client import client
from datetime import datetime, timedelta
from config import TOKEN, BanMeReplayAddress

bot = telebot.TeleBot(TOKEN, parse_mode=None)
bot_info = bot.get_me()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


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
        # 两个返回参数打包成数组保证一致性
        block_time = get_unix_time()[0]
        random_time = get_unix_time()[1]
        if str(bot.get_chat_member(message.chat.id, message.from_user.id).status) == "administrator" or "creator":
            bot.send_photo(message.chat.id, photo=BanMeReplayAddress, reply_to_message_id=message.chat.id)
        elif str(bot.get_chat_member(message.chat.id, message.from_user.id).status) == "member":
            bot.kick_chat_member(message.chat.id, message.from_user.id, block_time)
            bot.reply_to(message, "恭喜您获得" + str(random_time) + "秒禁言时间")


# 查询用户个人ID
@bot.message_handler(commands=['queryid'])
def query_user_id(message):
    if message.from_user.language_code == "zh-hans":
        bot.reply_to(message, "你的用户ID为：" + str(message.from_user.id))
    else:
        bot.reply_to(message, "Your User ID is:" + str(message.from_user.id))


@bot.message_handler(commands=['test'])
def test(message):
    # bot.reply_to(message, str(bot.get_chat(message.chat.id).id))
    bot.reply_to(message, client.get_all_group_member(message.chat.id))
    # bot.reply_to(message, str(bot.get_chat_members_count(message.chat.id)))


def get_unix_time():
    # 给定一个随机封禁秒数
    random_second = random.randint(100, 500)
    now_time = datetime.utcnow()
    # 处理时间
    process_time = now_time + timedelta(seconds=random_second)
    return [process_time, random_second]


bot.polling()
