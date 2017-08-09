# coding = utf8
from random import randint
import redis
from settings import *
from utils import *


class RedisClient(object):

    def __init__(self):
        try:
            if REDIS['password']:
                redis_pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'], password=REDIS['password'])
            else:
                redis_pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'])
            self._db = redis.Redis(connection_pool=redis_pool)
        except:
            send_error_msg('connect redis error')
        self._dbkey = 'ipproxy'
        self._dbkey_invalid = 'ipproxy:invalid'
        self._dbkey_source = 'ipproxy:source'
        self._dbkey_source_exists = 'ipproxy:source:exists'

    def get(self, count=1):
        proxies = []
        try:
            proxies = self._db.lrange(self._dbkey, 0, count-1)
            self._db.ltrim(self._dbkey, count, -1)
        except:
            send_error_msg('get proxy error, count:%s' % count)
        return proxies

    def put(self, proxy):
        try:
            proxies = self._db.lrange(self._dbkey, 0, self.queue_len)
            if proxy not in proxies:
                logging.info('PUT proxy {} INTO DB'.format(proxy))
                proxy = self._db.lpush(self._dbkey, proxy)
        except:
            send_error_msg('pop proxy error')

    def pop(self):
        proxy = ''
        try:
            proxy = self._db.rpop(self._dbkey).encode('utf8')
        except:
            send_error_msg('pop proxy error')
        return proxy

    def rand_proxy(self):
        try:
            index = randint(0, self.queue_len)
            proxies = self._db.lrange(self._dbkey, index, index+1)
            return proxies[0]
        except:
            pass
        return None

    def empty(self):
        self._db.delete(self._dbkey)

    @property
    def queue_len(self):
        return self._db.llen(self._dbkey)

    def save_invalid_proxy(self, proxy):
        if self._db.scard(self._dbkey_invalid) == 0:
            self._db.sadd(self._dbkey_invalid, proxy)
            self._db.expire(self._dbkey_invalid, INVALID_PROXY_EXPIRE)
        else:
            self._db.sadd(self._dbkey_invalid, proxy)

    def invalid_proxy_exists(self, proxy):
        return self._db.sismember(self._dbkey_invalid, proxy)

    def add_source_proxy(self, proxy):
        if not self._db.sismember(self._dbkey_source_exists, proxy):
            logging.info('Save {} into source proxy'.format(proxy))
            self._db.sadd(self._dbkey_source_exists, proxy)
            self._db.lpush(self._dbkey_source, proxy)

    def get_source_proxy(self, nums=5):
        try:
            proxies = []
            for i in xrange(5):
                proxy = self._db.rpop(self._dbkey_source)
                proxies.append(proxy)
                self._db.lpush(self._dbkey_source, proxy)
        except:
            pass
        return proxies


if __name__ == '__main__':
    conn = RedisClient()
    conn.put('xxxx')
    print(conn.pop())
