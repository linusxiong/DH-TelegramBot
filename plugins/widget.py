import re
from pyrogram import Client, filters
from others.dns_lookup import https, tls, udp
from others.package import check_delete_message_right, time_out, callback_func
from config import BOT_NAME
import requests


# 存活性测试
@Client.on_message(filters.incoming & filters.command(['ping', f'ping@{BOT_NAME}']))
def ping(client, message):
    send_message = message.reply_text("🏓️")
    check_delete_message_right(message, None, send_message)


# 查询用户ID
@Client.on_message(filters.incoming & filters.command(['queryid', f'queryid@{BOT_NAME}']))
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
@Client.on_message(filters.incoming & filters.command(['dc', f'dc@{BOT_NAME}']))
def query_user_id(client, message):
    if message.from_user is None:
        message.reply_text("❗**查询不到用户信息**")
    else:
        if message.from_user.language_code == "zh-hans":
            reply_message = message.reply_text(
                f"[{message.from_user.username}](tg://user?id={message.from_user.id})的数据中心为：**DC{str(message.from_user.dc_id)}**"
            )
        else:
            reply_message = message.reply_text(
                f"Your Account Datacenter is: **DC{str(message.from_user.dc_id)}**"
            )
        check_delete_message_right(message, reply_message, send_message=None)


# 查询IP信息
@Client.on_message(filters.incoming & filters.command(['ip', f'ip@{BOT_NAME}']))
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

                send_message = client.send_message(chat_id=message.chat.id, text=result, parse_mode="markdown")
            else:
                reply_message = message.reply_text("请求失败，请重试")
                check_delete_message_right(message, reply_message, None)

    else:
        reply_message = message.reply_text("请检查输入格式是否为IPv4")
        check_delete_message_right(message, reply_message, None)


@Client.on_message(filters.incoming & filters.private & filters.command(['doh', f'doh@{BOT_NAME}']))
# 装饰器限制函数运行时间，防止堵塞
@time_out(2, callback_func)
def doh_lookup(client, message):
    match_url = re.findall(r'(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message.text)
    match_nameserver = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/dns-query', message.text)
    # 匹配要解析的域名
    if match_url:
        url = match_url[1]
        nameserver = None
        # 匹配域名服务器
        if match_nameserver:
            nameserver = match_nameserver[0]
        lookup = https(domain=url, nameserver=nameserver)
        answer = '\n'.join(map(str, lookup['Answer']))
        reply = f"**查询方法**: {lookup['Method']}" \
                f"\n**域名**: \n{lookup['Domain']}" \
                f"\n**查询服务器**: \n{lookup['Nameserver']}" \
                f"\n**结果**: \n{answer}"
        send_message = client.send_message(chat_id=message.chat.id, text=reply, parse_mode="markdown")
    else:
        reply_message = message.reply_text("请检查输入格式是否正确")
        check_delete_message_right(message, reply_message, None)


@Client.on_message(filters.incoming & filters.private & filters.command(['dot', f'dot@{BOT_NAME}']))
# 装饰器限制函数运行时间，防止堵塞
@time_out(2, callback_func)
def dot_lookup(client, message):
    match_url = re.findall(r'(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message.text)
    match_tls = re.findall(r'tls://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message.text)
    match_ip = re.findall(r'\d+.\d+.\d+.\d+', message.text)
    if match_url:
        url = match_url[1]
        nameserver = None
        # 匹配tls链接格式
        if match_tls:
            nameserver = match_tls[0]
        if match_ip:
            nameserver = match_ip[0]
        lookup = tls(domain=url, nameserver=nameserver)
        answer = '\n'.join(map(str, lookup['Answer']))
        reply = f"**查询方法**: {lookup['Method']}" \
                f"\n**域名**: \n{lookup['Domain']}" \
                f"\n**查询服务器**: \n{lookup['Nameserver']}" \
                f"\n**结果**: \n{answer}"
        send_message = client.send_message(chat_id=message.chat.id, text=reply, parse_mode="markdown")
    else:
        reply_message = message.reply_text("请检查输入格式是否正确")
        check_delete_message_right(message, reply_message, None)


@Client.on_message(filters.incoming & filters.private & filters.command(['udp', f'udp@{BOT_NAME}']))
# 装饰器限制函数运行时间，防止堵塞
@time_out(2, callback_func)
def udp_lookup(client, message):
    match_url = re.findall(r'(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message.text)
    match_nameserver = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?["
                                  r"0-9][0-9]?)\b",
                                  message.text)
    if match_url:
        url = match_url[1]
        nameserver = None
        if match_nameserver:
            nameserver = match_nameserver[0]
        lookup = udp(domain=url, nameserver=nameserver)
        answer = '\n'.join(map(str, lookup['Answer']))
        reply = f"**查询方法**: {lookup['Method']}" \
                f"\n**域名**: \n{lookup['Domain']}" \
                f"\n**查询服务器**: \n{lookup['Nameserver']}" \
                f"\n**结果**: \n{answer}"
        send_message = client.send_message(chat_id=message.chat.id, text=reply, parse_mode="markdown")
    else:
        reply_message = message.reply_text("请检查输入格式是否正确")
        check_delete_message_right(message, reply_message, None)
