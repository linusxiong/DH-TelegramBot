from time import time
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import write_data, check_database, check_table, update_data_one, get_data_count, find_data


@Client.on_message(
    filters.incoming & ~filters.private & filters.command(['init', f'init@{BOT_NAME}']))
def database_initialization(client, message):
    # 防止匿名用户操作报错
    if message.from_user is None:
        message.reply_text("❗**查询不到用户信息**")
    else:
        # 如果数据库中存在同名表，表示已经初始化
        if check_table(message.chat.id, AllGroupMemberDatabaseName) is False:
            message.reply_text("❗**请勿重复初始化**")
        else:
            user_check = client.get_chat_member(message.chat.id, message.from_user.id)
            # 如果用户不是管理就不允许使用
            if user_check.status in ('administrator', 'creator'):
                user_filter = "all"
                send_message = message.reply_text("**初始化中，时间依照群组人数而定**")
                run_start = time()
                iter_chat = Client.iter_chat_members(self=client, chat_id=message.chat.id)
                if check_database(message.chat.id) and check_table(message.chat.id, AllGroupMemberDatabaseName):
                    all_group_member_list = []
                    for members in iter_chat:
                        all_group_member_dict = {
                            'ID': members.user.id,
                            'Username': members.user.username,
                            'Status': members.user.status,
                            'Identity': members.status,
                            'Until_date': members.until_date,
                            'Joined_date': members.joined_date,
                            'Bot': members.user.is_bot,
                            'Last_check_in_data': None
                        }
                        all_group_member_list.append(all_group_member_dict)
                    write_data(AllGroupMemberDatabaseName, message.chat.id, all_group_member_list)
                run_end = time()
                send_message.edit("**初始化完成, 总耗时{0:.2f}秒**".format(run_end - run_start))
            else:
                message.reply_text("**❗用户权限不足**")


@Client.on_message(
    filters.incoming & ~filters.private & filters.command(['update', f'update@{BOT_NAME}']))
def update_group_member(client, message):
    if message.from_user is None:
        message.reply_text("❗**查询不到用户信息**")
    else:
        user_check = client.get_chat_member(message.chat.id, message.from_user.id)
        if user_check.status in ('administrator', 'creator'):
            send_message = message.reply_text("**数据更新中**")
            iter_chat = Client.iter_chat_members(self=client, chat_id=message.chat.id)
            if check_database(message.chat.id) and check_table(message.chat.id, AllGroupMemberDatabaseName) is False:
                group_member_count = client.get_chat_members_count(message.chat.id)
                database_member_count = get_data_count(AllGroupMemberDatabaseName, message.chat.id)
                if group_member_count > database_member_count:
                    new_count = group_member_count - database_member_count
                    send_message = message.reply_text(
                        f"读取到{new_count}新用户数据，正在更新中"
                    )
                    update_start = time()
                    iter_chat = Client.iter_chat_members(self=client, chat_id=message.chat.id)
                    for members in iter_chat:
                        filter_find = {
                            'ID': members.user.id
                        }
                        data = find_data(AllGroupMemberDatabaseName, message.chat.id, filter_find)
                        if data is None:
                            all_group_member_list = []
                            all_group_member_dict = {
                                'ID': members.user.id,
                                'Username': members.user.username,
                                'Status': members.user.status,
                                'Identity': members.status,
                                'Until_date': members.until_date,
                                'Joined_date': members.joined_date,
                                'Bot': members.user.is_bot,
                                'Last_check_in_data': None
                            }
                            all_group_member_list.append(all_group_member_dict)
                            write_data(AllGroupMemberDatabaseName, message.chat.id, all_group_member_list)
                    update_end = time()
                    send_message = message.reply_text("**初始化完成, 总耗时{0:.2f}秒**".format(update_end - update_start))
            else:
                send_message.edit("**数据未初始化，请先初始化**")

        else:
            message.reply_text("**❗用户权限不足**")
