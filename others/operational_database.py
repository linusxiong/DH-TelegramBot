import pymongo
from plugins import error_code

# 数据库连接
client = pymongo.MongoClient('mongodb://localhost:27017/')


def check_database(chat_id):
    database_list = client.list_database_names()
    if chat_id in database_list:
        error_code.return_error(1001)
        return False
    else:
        return True


def check_table(chat_id, database_name):
    database = client[str(database_name)]
    table = database.list_collection_names()
    if chat_id in table:
        error_code.return_error(1002)
        return False
    else:
        return True


def check_data(database_name, chat_id, data):
    database = client[str(database_name)]
    table = database[str(chat_id)]
    if table is not None and data['_id'] == table.find_one({"_id": data['_id']})['_id']:
        error_code.return_error(1003)
        return False
    else:
        return True


def write_data(database_name, chat_id, data):
    database = client[str(database_name)]
    table = database[str(chat_id)]
    # 插入数据
    table.insert_many(data)


def update_data(database_name, chat_id, data, data_filter):
    database = client[str(database_name)]
    table = database[str(chat_id)]
    table.update_one(data_filter, data)


def find_data(database_name, chat_id, data_filter):
    database = client[str(database_name)]
    table = database[str(chat_id)]
    return table.find_one(data_filter)