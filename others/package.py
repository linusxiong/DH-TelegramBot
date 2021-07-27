from concurrent.futures import ThreadPoolExecutor
from time import sleep
from pyrogram.errors import MessageDeleteForbidden
from config import AUTO_DELETE
import threading
from plugins.error_code import return_error

executor = ThreadPoolExecutor(max_workers=40)


def callback_func():
    return return_error(1006)


def time_out(interval, callback=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            t = threading.Thread(target=func, args=args, kwargs=kwargs)
            t.setDaemon(True)  # 设置主线程技术子线程立刻结束
            t.start()
            t.join(interval)  # 主线程阻塞等待interval秒
            if t.is_alive() and callback:
                return threading.Timer(0, callback).start()  # 立即执行回调函数
            else:
                return

        return wrapper

    return decorator


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
