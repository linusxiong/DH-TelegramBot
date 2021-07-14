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
    TOKEN = '1826253371:AAFbV-ECTwwg2r7PZ-T1TIrg8tO9vsqG1rg'
    BanMeReplayAddress = "https://ae02.alicdn.com/kf/U54e2d33aa0694530897b008b097a5fb5U.png"
    api_id = 6692291
    api_hash = 'd37e4b6bb7af5e69e842ac0bcbab7e74'
    BOT_NAME = 'DH_TG_Bot'
    AllGroupMemberDatabaseName = 'group_data'