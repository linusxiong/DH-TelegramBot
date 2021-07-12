from pyrogram import Client, filters

api_id = 
api_hash = ''

with Client("my_account", api_id, api_hash) as app:
    def get_all_group_member(chat_id):
        list = []
        for member in app.iter_chat_members(chat_id):
            list.append(member.user.id)
            print(member.user.id)
        return list
        # all_group_member_dict = {"_id": member.user.id, 'ID': member.user.id,
        #                          'Username': member.user.username,
        #                          'Language': member.user.lang_code, 'Bot': member.user.bot}
# @Client.on_message(filters.incoming & ~filters.private & filters.command(['test']))
# def test(client, message):
#     # Iterate though all chat members
#     for member in app.iter_chat_members(message.chat.id):
#         print(member.user.first_name)

