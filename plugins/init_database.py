import asyncio
from time import time
from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import write_data, check_database, check_table, update_data_one, get_data_count, \
    find_data, delete_data_one, write_data_one


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
                    asyncio.run(write_data(AllGroupMemberDatabaseName, message.chat.id, all_group_member_list))
                run_end = time()
                send_message.edit("**初始化完成, 总耗时{0:.2f}秒**".format(run_end - run_start))
            else:
                message.reply_text("**❗用户权限不足**")


# 用户态检测
@Client.on_chat_member_updated()
def monitor_group_status(client, chat_member_updated):
    new_info = chat_member_updated.new_chat_member
    old_info = chat_member_updated.old_chat_member
    chat = chat_member_updated.chat
    if new_info and old_info is not None:

        # 成员被移除
        if new_info.status == 'kicked':
            info_filter = {
                'ID': new_info.user.id
            }
            asyncio.run(delete_data_one(AllGroupMemberDatabaseName, chat.id, info_filter))

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
            asyncio.run(write_data_one(AllGroupMemberDatabaseName, chat.id, new_group_member_dict))

        # 成员被限制
        if new_info.status == 'restricted' and old_info.status == 'member':
            user_filter = {
                'ID': new_info.user.id
            }
            update_group_member_dict = {
                "$set": {
                    'Identity': new_info.status,
                    'Until_date': new_info.until_date,
                }
            }
            asyncio.run(update_data_one(AllGroupMemberDatabaseName, chat.id, update_group_member_dict, user_filter))

        # 成员已解禁
        if new_info.status == 'member' and old_info.status == 'restricted' and old_info.restricted_by is not None:
            user_filter = {
                'ID': new_info.user.id
            }
            update_group_member_dict = {
                "$set": {
                    'Identity': new_info.status,
                    'Until_date': new_info.until_date,
                }
            }
            asyncio.run(update_data_one(AllGroupMemberDatabaseName, chat.id, update_group_member_dict, user_filter))

        # 用户变更为管理
        if old_info.status == 'member' and new_info.status == 'administrator':
            user_filter = {
                'ID': new_info.user.id
            }
            update_group_member_dict = {
                "$set": {
                    'Identity': new_info.status,
                    'Until_date': new_info.until_date,
                }
            }
            asyncio.run(update_data_one(AllGroupMemberDatabaseName, chat.id, update_group_member_dict, user_filter))
            send_message = client.send_message(chat.id, "检测到管理权限发生变动")

        # 用户由管理变成成员
        if old_info.status == 'administrator' and new_info.status == 'member':
            user_filter = {
                'ID': new_info.user.id
            }
            update_group_member_dict = {
                "$set": {
                    'Identity': new_info.status,
                    'Until_date': new_info.until_date,
                }
            }
            asyncio.run(update_data_one(AllGroupMemberDatabaseName, chat.id, update_group_member_dict, user_filter))
            send_message = client.send_message(chat.id, "检测到管理权限发生变动")

    if old_info is None:
        # 成员自行退出再进入
        if old_info is None and new_info.status == 'member':
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
            asyncio.run(write_data_one(AllGroupMemberDatabaseName, chat.id, new_group_member_dict))

    if new_info is None:
        # 成员自行退出
        if old_info.status == 'member' and new_info is None:
            info_filter = {
                'ID': old_info.user.id
            }
            asyncio.run(delete_data_one(AllGroupMemberDatabaseName, chat.id, info_filter))
