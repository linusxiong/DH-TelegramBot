from plugins import error_code
import motor.motor_asyncio
import pymongo


def check_database(chat_id):
    mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
    database_list = mongodb_client.list_database_names()
    mongodb_client.close()
    if str(chat_id) in database_list:
        error_code.return_error(1001)
        return False
    else:
        return True


def check_table(chat_id, database_name):
    mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = mongodb_client[str(database_name)]
    table = database.list_collection_names()
    mongodb_client.close()
    if str(chat_id) in table:
        error_code.return_error(1002)
        return False
    else:
        return True


def check_data(database_name, chat_id, data):
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    database = mongodb_client[str(database_name)]
    table = database[str(chat_id)]
    mongodb_client.close()
    if table is not None and data['_id'] == table.find_one({"_id": data['_id']})['_id']:
        error_code.return_error(1003)
        return False
    else:
        return True


async def write_data(database_name, chat_id, data):
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    database = mongodb_client[str(database_name)]
    table = database[str(chat_id)]
    # 插入数据
    await table.insert_many(data)
    mongodb_client.close()


async def write_data_one(database_name, chat_id, data):
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    database = mongodb_client[str(database_name)]
    table = database[str(chat_id)]
    # 插入数据
    await table.insert_one(data)
    mongodb_client.close()


async def update_data_one(database_name, chat_id, data, data_filter):
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    database = mongodb_client[str(database_name)]
    table = database[str(chat_id)]
    await table.update_one(data_filter, data)
    mongodb_client.close()


async def find_data(database_name, chat_id, data_filter):
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    database = mongodb_client[str(database_name)]
    table = database[str(chat_id)]
    result = await table.find_one(data_filter)
    mongodb_client.close()
    return result


async def get_data_count(database_name, chat_id):
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    database = mongodb_client[str(database_name)]
    table = database[str(chat_id)]
    result = await table.count
    mongodb_client.close()
    return result


async def delete_data_one(database_name, chat_id, data_filter):
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    database = mongodb_client[str(database_name)]
    table = database[str(chat_id)]
    await table.delete_one(data_filter)
    mongodb_client.close()
