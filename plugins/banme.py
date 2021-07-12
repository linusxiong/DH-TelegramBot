import random
from time import time, sleep
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions

from config import BanMeReplayAddress


@Client.on_message(filters.incoming & ~filters.private & filters.command(['banme']))
def banme(client, message):
    random_time = random.randint(100, 500)
    block_time = int(time() + random_time)
    permission = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_stickers=False,
        can_send_polls=False
    )
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != "member":
        message.reply_photo(photo=BanMeReplayAddress)
    else:
        try:
            send_message = message.reply_text("恭喜您获得" + str(block_time) + "秒禁言时间")
            client.restrict_chat_member(message.chat.id, message.from_user.id, permission, block_time)
        except ChatAdminRequired:
            send_message.edit("❗**无管理权限，请授予管理权限**")
            sleep(1)
        send_message.delete()
