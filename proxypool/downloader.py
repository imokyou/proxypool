# coding = utf8
import requests
from settings import *


def get_page(url, encodeing='utf8'):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        resp = requests.get(url, headers=headers, timeout=DOWNLOAD_TIMEOUT)
        if resp.status_code == 200:
            resp.encoding = encodeing
            return resp.text
        else:
            logging.info('{} response error, status_code: {}'.format(url, resp.status_code))
    except:
        logging.info('{} request timeout'.format(url))
    return None
