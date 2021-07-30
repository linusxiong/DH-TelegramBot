from time import time
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import write_data, check_database, check_table, update_data_one, get_data_count, \
    find_data, mongodb_client, delete_data_one


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
                if check_table(message.chat.id, AllGroupMemberDatabaseName):
                    all_group_member_list = []
                    for members in iter_chat:
                        all_group_member_dict = {
                            'ID': members.user.id,
                            'Username': members.user.username,
                            'User_status': members.user.status,
                            'Identity': members.status,
                            'Until_date': members.until_date,
                            'Joined_date': members.joined_date,
                            'DC_id': members.user.dc_id,
                            'Last_check_in_data': None
                        }
                        all_group_member_list.append(all_group_member_dict)
                    write_data(AllGroupMemberDatabaseName, message.chat.id, all_group_member_list)
                run_end = time()
                mongodb_client.close()
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
            if check_database(AllGroupMemberDatabaseName) is False and check_table(message.chat.id,
                                                                                   AllGroupMemberDatabaseName) is False:
                update_start = time()
                group_member_count = client.get_chat(message.chat.id).members_count
                database_member_count = get_data_count(AllGroupMemberDatabaseName, message.chat.id)
                if group_member_count > database_member_count:
                    new_count = group_member_count - database_member_count
                    send_message = message.reply_text(
                        f"读取到**{new_count}**新用户数据，正在更新中"
                    )

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
                    mongodb_client.close()
                    send_message = message.reply_text("**初始化完成, 总耗时{0:.2f}秒**".format(update_end - update_start))
                else:
                    send_message.edit("**未查询到新用户数据**")
            else:
                send_message.edit("**数据未初始化，请先初始化**")

        else:
            message.reply_text("**❗用户权限不足**")


# 用户态检测
@Client.on_chat_member_updated()
def monitor_group_status(client, chat_member_updated):
    new_info = chat_member_updated.new_chat_member
    old_info = chat_member_updated.old_chat_member
    chat = chat_member_updated.chat
    print(old_info)
    print("\n\n\n\n\n\n\n")
    print(new_info)
    if new_info and old_info is not None:

        # 成员被移除
        if new_info.status == 'kicked':
            info_filter = {
                'ID': new_info.user.id
            }
            delete_data_one(AllGroupMemberDatabaseName, chat.id, info_filter)
            print("成员被移除")
        # 新成员进入
        if new_info.status == 'member' and old_info.status != 'restricted' and old_info.status != 'administrator':
            new_group_member_dict = {
                'ID': new_info.user.id,
                'Username': new_info.user.username,
                'User_status': new_info.user.status,
                'Identity': new_info.status,
                'Until_date': new_info.until_date,
                'Joined_date': new_info.joined_date,
                'DC_id': new_info.user.dc_id,
                'Last_check_in_data': None
            }
            print("新成员进入")

        # 成员被限制
        if new_info.status == 'restricted' and old_info.status == 'member':
            print("成员被限制")

        # 成员已解禁
        if new_info.status == 'member' and old_info.status == 'restricted' and old_info.restricted_by is not None:
            print("成员已解禁")

        if old_info.status == 'member' and new_info.status == 'administrator':
            print("用户变更为管理")

        if old_info.status == 'administrator' and new_info.status == 'member':
            print("用户由管理变成成员")

    if old_info is None:
        # 成员自行退出再进入
        if old_info is None and new_info.status == 'member':
            print("新成员进入")

    if new_info is None:
        # 成员自行退出
        if old_info.status == 'member' and new_info is None:
            print("成员自己退出")
