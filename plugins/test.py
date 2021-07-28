from time import time

from config import BOT_NAME, AllGroupMemberDatabaseName
from pyrogram import Client, filters
from others.operational_database import write_data, check_database, check_table, update_data_one, get_data_count, \
    mongodb_client, find_data
from others.package import check_delete_message_right


@Client.on_message(filters.incoming & filters.command(['test', f'test@{BOT_NAME}']))
def test(client, message):
    group_member_count = client.get_chat(message.chat.id).members_count
    print(group_member_count)
    update_start = time()
    database_member_count = get_data_count(AllGroupMemberDatabaseName, message.chat.id)
    print(database_member_count)
    update_end = time()
    send_message = message.reply_text("**初始化完成, 总耗时{0:.2f}秒**".format(update_end - update_start))
    # group_member_count = client.get_chat_members_count(message.chat.id)
    # database_member_count = get_data_count(AllGroupMemberDatabaseName, message.chat.id)
    # if group_member_count > database_member_count:
    #     new_count = group_member_count - database_member_count
    #     send_message = message.reply_text(
    #         f"读取到{new_count}新用户数据，正在更新中"
    #     )
    #     check_delete_message_right(message, None, send_message)
    #     run_start = time()
    #     iter_chat = Client.iter_chat_members(self=client, chat_id=message.chat.id)
    #     for members in iter_chat:
    #         filter_find = {
    #             'ID': members.user.id
    #         }
    #         data = find_data(AllGroupMemberDatabaseName, message.chat.id, filter_find)
    #         if data is None:
    #             all_group_member_list = []
    #             all_group_member_dict = {
    #                 'ID': members.user.id,
    #                 'Username': members.user.username,
    #                 'Status': members.user.status,
    #                 'Identity': members.status,
    #                 'Until_date': members.until_date,
    #                 'Joined_date': members.joined_date,
    #                 'Bot': members.user.is_bot,
    #                 'Last_check_in_data': None
    #             }
    #             all_group_member_list.append(all_group_member_dict)
    #             write_data(AllGroupMemberDatabaseName, message.chat.id, all_group_member_list)
    #     run_end = time()
    #     send_message = message.reply_text("**初始化完成, 总耗时{0:.2f}秒**".format(run_end - run_start))
    #     check_delete_message_right(message, None, send_message)