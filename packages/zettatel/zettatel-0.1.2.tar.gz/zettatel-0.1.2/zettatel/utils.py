
import requests


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
