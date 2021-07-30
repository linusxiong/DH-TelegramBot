import re

from fastapi import FastAPI
from typing import Optional
from pyrogram import Client, filters
import sys
sys.path.append('..')
from plugins.error_code import return_error
from others.dns_lookup import https, udp, tls
from others.package import time_out, callback_func
app = FastAPI()


@app.get("/api")
async def root():
    return {"message": "Welcome to use the DH-BOT"}


@app.get("/api/getChat/{chat_id}")
@Client.on_message()
async def get_chat(chat_id: int, client, message):
    return {"message": client.get_me()}


@app.get("/api/dns/{dns_type}")
async def dns_lookup_api(dns_type, domain: str, nameserver: Optional[str] = None):

    def udp_switch(domain_fun, nameserver_fun):
        udp_look_up = udp(domain_fun, nameserver_fun)
        answer = ' '.join(map(str, udp_look_up['Answer']))
        return {
            'Method': udp_look_up['Method'],
            'Domain': udp_look_up['Domain'],
            'Nameserver': udp_look_up['Nameserver'],
            'Answer': answer
        }

    def https_switch(domain_fun, nameserver_fun):
        udp_look_up = https(domain_fun, nameserver_fun)
        answer = ' '.join(map(str, udp_look_up['Answer']))
        return {
            'Method': udp_look_up['Method'],
            'Domain': udp_look_up['Domain'],
            'Nameserver': udp_look_up['Nameserver'],
            'Answer': answer
        }


    # def tls_switch(domain_fun, nameserver_fun):
    #     udp_look_up = tls(domain_fun, nameserver_fun)
    #     answer = ' '.join(map(str, udp_look_up['Answer']))
    #     return {
    #         'Method': udp_look_up['Method'],
    #         'Domain': udp_look_up['Domain'],
    #         'Nameserver': udp_look_up['Nameserver'],
    #         'Answer': answer
    #     }
    def tls_switch(domain_fun, namserver_fun):
        match_tls = re.findall(r'tls://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', namserver_fun)
        match_ip = re.findall(r'\d+.\d+.\d+.\d+', namserver_fun)
        nameserver_fun = None
        if match_tls:
            nameserver_fun = match_tls[0]
        if match_ip:
            nameserver_fun = match_ip[0]
        lookup = tls(domain=domain_fun, nameserver=nameserver_fun)
        answer = '\n'.join(map(str, lookup['Answer']))
        reply = f"**查询方法**: {lookup['Method']}" \
                f"\n**域名**: \n{lookup['Domain']}" \
                f"\n**查询服务器**: \n{lookup['Nameserver']}" \
                f"\n**结果**: \n{answer}"

    ways = {
        "udp": udp_switch(domain, nameserver),
        "https": https_switch(domain, nameserver),
        "tls": tls_switch(domain, nameserver),
    }

    return ways.get(dns_type)
