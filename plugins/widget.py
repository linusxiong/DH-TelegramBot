import re
from pyrogram import Client, filters
from others.package import check_delete_message_right
from config import BOT_NAME
import requests


# 存活性测试
@Client.on_message(filters.incoming & filters.command(['ping', 'ping@{bot_name}'.format(bot_name=BOT_NAME)]))
def ping(client, message):
    send_message = message.reply_text("🏓️")
    check_delete_message_right(message, None, send_message)


# 查询用户ID
@Client.on_message(filters.incoming & filters.command(['queryid', 'queryid@{bot_name}'.format(bot_name=BOT_NAME)]))
def query_id(client, message):
    if message.from_user is None:
        message.reply_text("❗**查询不到用户信息**")
    else:
        if message.from_user.language_code == "zh-hans":
            reply_message = message.reply_text("你的用户ID为：" + str(message.from_user.id))
        else:
            reply_message = message.reply_text("Your User ID is:" + str(message.from_user.id))
        check_delete_message_right(message, reply_message, send_message=None)


# 查询用户数据中心
@Client.on_message(filters.incoming & filters.command(['dc', 'dc@{bot_name}'.format(bot_name=BOT_NAME)]))
def query_user_id(client, message):
    if message.from_user is None:
        message.reply_text("❗**查询不到用户信息**")
    else:
        if message.from_user.language_code == "zh-hans":
            reply_message = message.reply_text(
                "[{}](tg://user?id={})的数据中心为：**DC{}**".format(message.from_user.username, message.from_user.id,
                                                              str(message.from_user.dc_id)))
        else:
            reply_message = message.reply_text(
                "Your Account Datacenter is: **DC{}**".format(str(message.from_user.dc_id)))
        check_delete_message_right(message, reply_message, send_message=None)


# 查询IP信息
@Client.on_message(filters.incoming & filters.command(['ip', 'ip@{bot_name}'.format(bot_name=BOT_NAME)]))
def query_ip_information(client, message):
    url = 'https://api.ip.sb/geoip/'
    match = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                       message.text)
    if match:
        for ip in match:
            response = requests.get(url + ip)
            if response.status_code == 200:
                json_dict = response.json()
                for index in ('country', 'region', 'city'):
                    if index not in json_dict:
                        json_dict[index] = ''

                data = {
                    'ip': json_dict['ip'],
                    'country': json_dict['country'],
                    'region': json_dict['region'],
                    'city': json_dict['city'],
                    'asn': json_dict['asn'],
                    'asn_organization': json_dict['asn_organization'],
                    'isp': json_dict['isp'],
                    'organization': json_dict['organization']
                }
                result = "**查询目标**: {ip}" \
                         "\n**地理位置**: {country} {region} {city}" \
                         "\n**运营商**: {isp}" \
                         "\n**ASN**: [AS{asn} {asn_organization}](https://bgp.he.net/AS{asn})".format(**data)

                reply_message = message.reply_text(result, parse_mode="markdown")
                check_delete_message_right(message, reply_message, None)
            else:
                reply_message = message.reply_text("请求失败，请重试")
                check_delete_message_right(message, reply_message, None)

    else:
        reply_message = message.reply_text("请检查输入格式是否为IPv4")
        check_delete_message_right(message, reply_message, None)

# # 查询WHOIS
# @Client.on_message(filters.incoming & filters.command(['whois', 'whois@{bot_name}'.format(bot_name=BOT_NAME)]))
# def query_whois(client, message):
#
