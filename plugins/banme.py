import random
from time import time
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid
from pyrogram.types import ChatPermissions
from config import BanMeReplayAddress, BOT_NAME
from others.package import check_delete_message_right


@Client.on_message(
    filters.incoming & ~filters.private & filters.command(['banme', f'banme@{BOT_NAME}']))
def banme(client, message):
    try:
        random_time = random.randint(100, 500)
        block_time = int(time() + random_time)
        permission = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_stickers=False,
            can_send_polls=False
        )
        if message.from_user is None:
            message.reply_text("❗**查询不到用户信息**")
        else:
            user = client.get_chat_member(message.chat.id, message.from_user.id)
            if user.status in ('administrator', 'creator'):
                reply_message = message.reply_photo(photo=BanMeReplayAddress)
                check_delete_message_right(message, reply_message, send_message=None)
            else:
                send_message = message.reply_text("恭喜您获得" + str(random_time) + "秒禁言时间")
                client.restrict_chat_member(message.chat.id, message.from_user.id, permission, block_time)
    except (ChatAdminRequired, UserAdminInvalid):
            send_message.edit("❗**无权限，请授予相应权限**")
            check_delete_message_right(message, None, send_message)


# 解除封禁
@Client.on_message(
    filters.incoming & ~filters.private & filters.command(['unban', f'unban@{BOT_NAME}']))
def unban(client, message):
    try:
        if message.reply_to_message is not None:
            send_message = message.reply_text(
                "已解除[{}](tg://user?id={})的封禁".format(message.reply_to_message.from_user.first_name,
                                                     message.reply_to_message.from_user.id))
            client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        else:
            send_message = message.reply_text("❗**被删除用户未知，请回复被踢者消息踢除**")
    except ChatAdminRequired:
        send_message.edit("❗**无管理权限，请授予管理权限**")
    check_delete_message_right(message, None, send_message)


# 永久踢人
@Client.on_message(
    filters.incoming & ~filters.private & filters.command(['kick', f'kick@{BOT_NAME}']))
def kick_people(client, message):
    try:
        if message.reply_to_message is not None:
            send_message = message.reply_text(
                "已永久踢除[{}](tg://user?id={})".format(message.reply_to_message.from_user.first_name,
                                                    message.reply_to_message.from_user.id))
            client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        else:
            send_message = message.reply_text("❗**被删除用户未知，请回复被踢者消息踢除**")
    except ChatAdminRequired:
        send_message.edit("❗**无管理权限，请授予管理权限**")
    check_delete_message_right(message, None, send_message)
