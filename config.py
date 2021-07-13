import os

ENV = bool(os.environ.get('ENV', False))
if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    BanMeReplayAddress = os.environ.get("BanMeReplayAddress", None)
    api_id = os.environ.get("api_id", None)
    api_hash = os.environ.get("api_hash", None)
    BOT_NAME = os.environ.get("BOT_NAME", None)
    AllGroupMemberDatabaseName = os.environ.get("AllGroupMemberDatabaseName", None)
else:
    TOKEN = ''
    BanMeReplayAddress = ""
    api_id = 
    api_hash = ''
    BOT_NAME = ''
    AllGroupMemberDatabaseName = ''