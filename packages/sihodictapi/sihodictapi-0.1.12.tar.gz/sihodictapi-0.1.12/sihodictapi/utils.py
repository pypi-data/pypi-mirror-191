import hashlib

from requestspr import Requests

requests = Requests()


def request_get(url, params=None, **kwargs):
    return requests.get(url, params, **kwargs)


def request_post(url, data=None, json=None, **kwargs):
    return requests.post(url, data, json, **kwargs)


def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()
