import requests
import re
from .utils import is_date, send_request


def send_sms(userid, password,  senderid, output, duplicatecheck, msg: str, **kwargs):
    extr = kwargs
    url = "https://portal.zettatel.com/SMSApi/send"

    payload = {'userid': userid,
               'password': password,
               'senderid': senderid,
               'msg': msg,
               'sendMethod': 'quick',
               'msgType': 'text',
               'output': output,
               'duplicatecheck': duplicatecheck}

    if kwargs.get('group'):
        payload['group'] = extr['group']

    elif kwargs.get('to'):
        payload['mobile'] = extr['to']

    if extr.get('scheduleTime'):
        if is_date(extr['scheduleTime']):
            payload['scheduleTime'] = extr['scheduleTime']
        else:
            return ValueError("Invalid date and time")
    elif extr.get('smartLinkTitle'):
        payload['smartLinkTitle'] = extr['smartLinkTitle']

    files = [

    ]
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    print(response.text)

    return response
