from time import sleep
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import write_data, check_database, check_table


@Client.on_message(filters.incoming & ~filters.private & filters.command(['init', 'init@{bot_name}'.format(bot_name=BOT_NAME)]))
def database_initialization(client, message):
    user_check = client.get_chat_member(message.chat.id, message.from_user.id)
    if user_check.status in ('administrator', 'creator'):
        user_filter = "all"
        send_message = message.reply_text("**初始化中，时间依照群组人数而定**")
        iter_chat = Client.iter_chat_members(self=client, chat_id=message.chat.id, filter=user_filter)
        if check_database(message.chat.id) and check_table(message.chat.id, AllGroupMemberDatabaseName):
            all_group_member_list = []
            for members in iter_chat:
                all_group_member_dict = {
                    "_id": members.user.id,
                    'Username': members.user.username,
                    'Status': members.user.status,
                    'Identity': members.status,
                    'Until_date': members.until_date,
                    'Joined_date': members.joined_date,
                    'Bot': members.user.is_bot
                }
                all_group_member_list.append(all_group_member_dict)

            write_data(AllGroupMemberDatabaseName, message.chat.id, all_group_member_list)
        send_message.edit("**初始化完成**")
    else:
        reply_message = message.reply_text("**❗用户权限不足**")
