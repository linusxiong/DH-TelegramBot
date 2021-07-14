from time import sleep, time
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import write_data, check_database, check_table


@Client.on_message(filters.incoming & ~filters.private & filters.command(['init', 'init@{bot_name}'.format(bot_name=BOT_NAME)]))
def database_initialization(client, message):
    if message.from_user is None:
        reply_message = message.reply_text("❗**查询不到用户信息**")
    else:
        user_check = client.get_chat_member(message.chat.id, message.from_user.id)
        if user_check.status in ('administrator', 'creator'):
            user_filter = "all"
            send_message = message.reply_text("**初始化中，时间依照群组人数而定**")
            run_start = time()
            iter_chat = Client.iter_chat_members(self=client, chat_id=message.chat.id)
            if check_database(message.chat.id) and check_table(message.chat.id, AllGroupMemberDatabaseName):
                # print(Client.get_chat_members_count(self=client, chat_id=message.chat.id))
                all_group_member_list = []
                for members in iter_chat:
                    all_group_member_dict = {
                        "ID": members.user.id,
                        'Username': members.user.username,
                        'Status': members.user.status,
                        'Identity': members.status,
                        'Until_date': members.until_date,
                        'Joined_date': members.joined_date,
                        'Bot': members.user.is_bot,
                        "Last_check_in_data": None
                    }
                    # print(all_group_member_dict)
                    all_group_member_list.append(all_group_member_dict)
                write_data(AllGroupMemberDatabaseName, message.chat.id, all_group_member_list)
            run_end = time()
            # print(run_end - run_start)
            send_message.edit("**初始化完成, 总耗时{0:.2f}秒**".format(run_end - run_start))
        else:
            message.reply_text("**❗用户权限不足**")
