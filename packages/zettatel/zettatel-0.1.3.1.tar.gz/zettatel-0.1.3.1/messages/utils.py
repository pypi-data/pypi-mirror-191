import requests
from dateutil.parser import parse
import re


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def is_url(link):
    """
    Checks if a supplied string is a valid url
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, link) is not None


def send_request(url, method, payload=None, headers=None, file=None):
    request_body = {}
    files = {}
    header = {}

    if payload:
        request_body.update(payload)
    if headers:
        header.update(headers)
    if file:
        files.update(file)

    response = requests.request(
        method, url, headers=header, data=request_body, files=files)

    return response
