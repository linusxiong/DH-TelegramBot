import random
from time import time, sleep
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, MessageDeleteForbidden, UserAdminInvalid
from pyrogram.types import ChatPermissions

from config import BanMeReplayAddress, BOT_NAME


@Client.on_message(filters.incoming & ~filters.private & filters.command(['banme', 'banme@{bot_name}'.format(bot_name=BOT_NAME)]))
def banme(client, message):
    random_time = random.randint(100, 500)
    block_time = int(time() + random_time)
    permission = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_stickers=False,
        can_send_polls=False
    )
    if message.from_user.id is None:
        message.reply_text("")
    else:
        user = client.get_chat_member(message.chat.id, message.from_user.id)
    try:
        if user.status in ('administrator', 'creator'):
            reply_message = message.reply_photo(photo=BanMeReplayAddress)
            # 自动删除信息
            sleep(5)
            message.delete()
            reply_message.delete()
    except MessageDeleteForbidden:
            reply_message.edit("❗**无删除用户信息权限，请授予管理权限**")
    else:
        try:
            send_message = message.reply_text("恭喜您获得" + str(random_time) + "秒禁言时间")
            client.restrict_chat_member(message.chat.id, message.from_user.id, permission, block_time)
        except (ChatAdminRequired, UserAdminInvalid):
            send_message.edit("❗**无管理权限，请授予管理权限**")
        # 自动删除信息
        sleep(5)
        message.delete()
        send_message.delete()