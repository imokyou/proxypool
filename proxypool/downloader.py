# coding = utf8
from random import randint
import requests
from settings import *
from db import RedisClient


def get_proxy():
    try:
        conn = RedisClient()
        proxy = conn.rand_proxy()
        proxies = {
            proxy[0:4]: proxy
        }
        return proxies
    except:
        pass
    return None


def get_headers():
    headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        },
        {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }
    ]
    return headers[randint(0, len(headers)-1)]


def get_page(url, encodeing='utf8'):
    try:
        logging.info('get proxy from {}'.format(url))
        headers = get_headers()
        resp = requests.get(url, headers=headers, timeout=DOWNLOAD_TIMEOUT)
        if not resp or resp.status_code != 200:
            raise Exception('request error')
    except:
        logging.info('{} request error, try again'.format(url))
        proxies = get_proxy()
        resp = requests.get(url, headers=headers, proxies=proxies,timeout=DOWNLOAD_TIMEOUT)
    if resp and resp.status_code == 200:
        resp.encoding = encodeing
        return resp.text
    else:
        logging.info('{} response error, status_code: {}'.format(url, resp.status_code))
    return None
