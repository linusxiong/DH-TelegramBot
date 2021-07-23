from concurrent.futures import ThreadPoolExecutor
from time import sleep
from pyrogram.errors import MessageDeleteForbidden

from config import AUTO_DELETE

executor = ThreadPoolExecutor(max_workers=40)


def check_delete_message_right(message, reply_message, send_message):
    if AUTO_DELETE:
        executor.submit(work, message, reply_message, send_message)


def work(message, reply_message, send_message):
    wait_time = 10
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
