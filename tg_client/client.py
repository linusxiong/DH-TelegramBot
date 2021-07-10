from telethon.sync import TelegramClient
api_id = 
api_hash = ''
client = TelegramClient('simple_user_bot', api_id, api_hash)
client.connect()


def get_all_group_member(chat_id, count):
    all_participants = client.get_participants(chat_id)
    for index in range(count):
        all_group_member_dict = {'ID': all_participants[index].id, 'Username': all_participants[index].username,
                                     'Language': all_participants[index].lang_code, 'Bot': all_participants[index].bot}
        print(all_group_member_dict)
    # database.write_data("group_member", chat_id, all_group_member_dict)


# get_all_group_member(-1001196317569, 11)
