import hashlib

import requestspr as requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def request_get(url, params=None):
    return requests.get(url, params, headers=headers, timeout=(5, 5))


def request_post(url, data=None, json=None):
    return requests.post(url, data, json, headers=headers, timeout=(5, 5))


def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()
