import re
import dns.query
from dns import rdatatype, message
import requests
import requests_toolbelt
from urllib.parse import urlparse
from plugins.error_code import return_error


def udp(domain, nameserver=None, port=None):
    domain_pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )

    if nameserver is None:
        nameserver = "223.5.5.5"
    if port is None:
        port = 53
    if domain_pattern.match(domain):
        query = message.make_query(domain, rdatatype.A)
        response = dns.query.udp(query, nameserver, port=port)
        answer_list = []
        for answer in response.answer:
            for index in range(len(answer)):
                answer_list.append(answer[index])
        https_answer_dict = {
            'Method': "UDP",
            'Domain': domain,
            'Nameserver': nameserver,
            'Answer': answer_list
        }
        return https_answer_dict
    else:
        return return_error(1005)


def https(domain, nameserver=None, port=None):
    if nameserver is None:
        nameserver = 'https://223.5.5.5/dns-query'
    if port is None:
        port = 443
    if re.match(r'^https?:/{2}\w.+/dns-query$', nameserver):
        with requests.sessions.Session() as session:
            query = message.make_query(domain, rdatatype.A)
            response = dns.query.https(query, nameserver, port, session=session)
            answer_list = []
            for answer in response.answer:
                for index in range(len(answer)):
                    answer_list.append(answer[index])

            https_answer_dict = {
                'Method': "HTTPS",
                'Domain': domain,
                'Nameserver': nameserver,
                'Answer': answer_list
            }
            return https_answer_dict
    else:
        return return_error(1005)


def tls(domain, port=None, nameserver=None):
    if port is None:
        port = 853
    if nameserver is None:
        nameserver = "223.5.5.5"
    if re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                  nameserver):
        nameserver = nameserver
    else:
        parse_result = urlparse(nameserver)
        nameserver = parse_result.hostname
        nameserver = udp(nameserver)['Answer'][0].to_text()

    query = message.make_query(domain, rdatatype.A)
    response = dns.query.tls(query, nameserver, port=port)
    answer_list = []
    for answer in response.answer:
        for index in range(len(answer)):
            answer_list.append(answer[index])

    tls_answer_dict = {
        'Method': "TLS",
        'Domain': domain,
        'Nameserver': nameserver,
        'Answer': answer_list
    }
    return tls_answer_dict
