from time import sleep

from pyrogram.errors import MessageDeleteForbidden


def check_delete_message_right(message, reply_message, send_message):
    wait_time = 30
    try:
        sleep(wait_time)
        message.delete()
        if reply_message is None:
            pass
        else:
            reply_message.delete()

        if send_message is None:
            pass
        else:
            send_message.delete()
    except MessageDeleteForbidden:
        if reply_message is None:
            pass
        else:
            reply_message.edit("❗**无删除用户信息权限，请授予管理权限**")

        if send_message is None:
            pass
        else:
            send_message.edit("❗**无删除用户信息权限，请授予管理权限**")