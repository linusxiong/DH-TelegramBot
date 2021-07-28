from config import TOKEN, api_id, api_hash
from pyrogram import Client

plugins = dict(
    root="plugins",
    include=[
        "auto_kick_people",
        "init_database",
        "help",
        "banme",
        "check_in",
        "widget"
    ]
)
app = Client(
    'DH-Bot',
    bot_token=TOKEN,
    api_id=api_id,
    api_hash=api_hash,
    plugins=plugins
)
app.run()

