# coding = utf8
import math
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import requests
from time import sleep
from multiprocessing import Process
from settings import *
from db import RedisClient
from spider import ProxySpider
from utils import *


class ProxyTester(object):

    def __init__(self):
        self._raw_proxies = []
        self._unuseable_proxies = []

    def set_row_proxies(self, proxies):
        self._raw_proxies = proxies

    @staticmethod
    def test_single_proxy(args):
        try:
            conn = args[0]
            proxy = args[1].lower()
            if conn.invalid_proxy_exists(proxy):
                logging.info('proxy {} is invalid, will be checked after a couple hours'.format(proxy))
                return None
            ip = proxy.replace('http://', '').replace('https://', '').split(':')[0]
            if not is_ip_valid(ip):
                logging.info('invalid proxy %s' % proxy)
                return None
            proxies = {
                proxy[0:4]: proxy
            }
            resp = requests.get(TEST_API, proxies=proxies, timeout=5)
            if resp.status_code == 200:
                logging.info('Valid proxy %s' % proxy)
                conn.put(proxy)
            else:
                logging.info('invalid proxy %s' % proxy)
                conn.save_invalid_proxy(proxy)
        except:
            logging.info('invalid proxy %s' % proxy)
            conn.save_invalid_proxy(proxy)
        sleep(1)

    def test(self):
        pool = Pool(5)
        conn = RedisClient()
        pool.map(ProxyTester.test_single_proxy, [(conn, x) for x in self._raw_proxies])


class PoolAdder(object):

    def __init__(self, threshold_upper):
        self._threshold_upper = threshold_upper
        self._conn = RedisClient()
        self._tester = ProxyTester()
        self._spider = ProxySpider()

    def is_lower_threshold(self):
        return self._conn.queue_len < self._threshold_upper

    def is_upper_threshold(self):
        return self._conn.queue_len >= self._threshold_upper

    def add_to_queue(self):
        while self.is_lower_threshold():
            for callback in self._spider.__CrawlFunc__:
                proxies = self._spider.get_raw_proxies(callback)
                self._tester.set_row_proxies(proxies)
                self._tester.test()
                sleep(30)
                if self.is_upper_threshold():
                    break


class Schedule(object):
    @staticmethod
    def valid_proxy(run_cycle=RUN_CYCLE):
        logging.debug('start valid proxy...')
        conn = RedisClient()
        tester = ProxyTester()
        while True:
            if not conn.queue_len:
                sleep(run_cycle)
                logging.info('ValidProxy: There is no proxy in pool')
                continue
            proxies = conn.get(int(math.ceil(0.5*conn.queue_len)))
            tester.set_row_proxies(proxies)
            tester.test()
            sleep(run_cycle)

    @staticmethod
    def check_pool(threshold_lower=THRESHOLD_LOWER,
                   threshold_upper=THRESHOLD_UPPER,
                   run_cycle=RUN_CYCLE):
        logging.debug('start check pool...')
        conn = RedisClient()
        adder = PoolAdder(threshold_upper)
        while True:
            if conn.queue_len <= threshold_upper:
                adder.add_to_queue()
            else:
                logging.info('CheckPool: Proxypool is enough')
            sleep(run_cycle)

    def run(self):
        logging.info('IP Proxy proces start runing')
        valid_process = Process(target=Schedule.valid_proxy)
        check_process = Process(target=Schedule.check_pool)

        valid_process.start()
        check_process.start()


if __name__ == '__main__':
    s = Schedule()
    s.run()
