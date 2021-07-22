from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

help_message = [
    ".",

    "**DH-Bot**"
    "\n使用前先给予DH-Bot管理员权限"
    "\n使用机器人之前请先在**群组内**进行初始化操作"
    "\n```/init``` 初始化"
    "\n不进行初始化操作将无法使用群组内签到等功能"
    "\n下一页查看所有指令",

    "**Command**"
    "\n```/init``` 初始化"
    "\n```/update``` 更新群组数据库"
    "\n```/auto_hick``` 根据输入指令自动踢出"
    "\n```/group_status``` 获取群组状态"
    "\n```/kick_deleted``` 删除群组中所有已删除账户"
    "\n```/banme``` 获得随机封禁时长"
    "\n```/unban``` 解除封禁"
    "\n```/kick_people``` 永久踢除"
    "\n```/ip``` 查询IP信息(arguments)"
    "\n/dc 查询Datacenter位置"
    "\n/queryid 查询用户ID"
    "\n/ping 存活测试"
    "\n```/check_in``` 签到(根据群组)"
    "\n```/auto_kick``` (arguments)"
    "\n\n下一页查看详细指令用法",


    "**Arguments**"
    "\n“online” - 删除在线用户"
    "\n“offline” - 踢出所有在线用户"
    "\n“recently” - 踢出最近3天内未上线用户(慎重)"
    "\n“within_week” - 踢出2-3天或者一星期内未上线用户 "
    "\n“within_month” - 踢出6-7天或者一个月内未上线用户"
    "\n“long_time_ago” - 踢出超过一个月未上线用户"
    "\n\n下一页查看例子",

    "**Examples**"
    "\n```/auto_kick long_time_ago``` - 删除超过一个月未登录用户"
    "\n```/kick_deleted``` - 踢出已删除账户"
    "\n ```/ip 8.8.8.8``` - 查询8.8.8.8的信息",

    "**Developer - @dalao2333**"
]


start_message = "**尊敬的用户 [{}](tg://user?id={})**\n欢迎使用DH-Bot，更多查看 /help"


@Client.on_message(filters.private & filters.incoming & filters.command(['start']))
def _start(client, message):
    client.send_message(message.chat.id,
                        text=start_message.format(message.from_user.first_name, message.from_user.id),
                        parse_mode="markdown",
                        reply_to_message_id=message.message_id
                        )


@Client.on_message(filters.private & filters.incoming & filters.command(['help']))
def _help(client, message):
    client.send_message(chat_id=message.chat.id,
                        text=help_message[1],
                        parse_mode="markdown",
                        disable_notification=True,
                        reply_markup=InlineKeyboardMarkup(map(1)),
                        reply_to_message_id=message.message_id
                        )


help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))


@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    message = int(callback_query.data.split('+')[1])
    client.edit_message_text(chat_id=chat_id, message_id=message_id,
                             text=help_message[message], reply_markup=InlineKeyboardMarkup(map(message))
                             )


def map(page):
    if page == 1:
        button = [
            [InlineKeyboardButton(text='-->', callback_data="help+2")]
        ]
    elif page == len(help_message) - 1:
        button = [
            [InlineKeyboardButton(text='联系作者', url="https://t.me/dalao2333")],
            [InlineKeyboardButton(text='<--', callback_data=f"help+{page - 1}")]
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text='<--', callback_data=f"help+{page - 1}"),
                InlineKeyboardButton(text='-->', callback_data=f"help+{page + 1}")
            ],
        ]
    return button
