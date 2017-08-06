# coding = utf8
from time import sleep
from downloader import get_page
from bs4 import BeautifulSoup
from settings import *


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['__CrawlFuncCount__'] = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                attrs['__CrawlFuncCount__'] = attrs['__CrawlFuncCount__'] + 1
        return type.__new__(cls, name, bases, attrs)


class ProxySpider(object):
    __metaclass__ = ProxyMetaClass

    def get_raw_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, pages=5, encodeing='gb2312'):
        start_url = 'http://www.66ip.cn/{}.html'
        for page in xrange(1, pages+1):
            html = get_page(start_url.format(page), encodeing=encodeing)
            if html:
                bs = BeautifulSoup(html, 'lxml')
                iptrs = bs.select('.containerbox table tr')
                i = 0
                for tr in iptrs:
                    if i == 0:
                        i = i + 1
                        continue
                    ip = tr.select('td:nth-of-type(1)')[0].get_text().encode('utf8')
                    port = tr.select('td:nth-of-type(2)')[0].get_text().encode('utf8')
                    i = i + 1
                    yield 'http://{}:{}'.format(ip, port)
            sleep(30)

    def crawl_xici(self, pages=5):
        start_url = 'http://www.xicidaili.com/wt/{}'
        for page in xrange(1, pages+1):
            html = get_page(start_url.format(page))
            if html:
                bs = BeautifulSoup(html, 'lxml')
                iptrs = bs.select('#ip_list tr')
                i = 0
                for tr in iptrs:
                    if i == 0:
                        i = i + 1
                        continue
                    ip = tr.select('td:nth-of-type(2)')[0].get_text().encode('utf8')
                    port = tr.select('td:nth-of-type(3)')[0].get_text().encode('utf8')
                    proto = tr.select('td:nth-of-type(6)')[0].get_text().encode('utf8').lower()
                    i = i + 1
                    yield '{}://{}:{}'.format(proto, ip, port)
            sleep(30)

    def crawl_goubanjia(self, pages=5):
        start_url = 'http://www.goubanjia.com/free/gngn/index{}.shtml'
        for page in xrange(1, pages+1):
            html = get_page(start_url.format(page))
            if html:
                bs = BeautifulSoup(html, 'lxml')
                iptds = bs.select('td.ip')
                for td in iptds:
                    ip = []
                    for t in td:
                        if t.name not in ['span', 'div'] or not t.string or t.attrs.get('style') == 'display: none;':
                            continue
                        ip.append(t.string)
                    yield 'http://{}:{}'.format(''.join(ip[0:-2]), ip[-1])
            sleep(30)

    def crawl_proxy360(self):
        start_url = 'http://www.proxy360.cn/Region/China'
        html = get_page(start_url)
        if html:
            bs = BeautifulSoup(html, 'lxml')
            ipdivs = bs.select('div.proxylistitem')
            i = 0
            for tr in ipdivs:
                if i == 0:
                    i = i + 1
                    continue
                ip = tr.select('div span:nth-of-type(1)')[0].get_text().encode('utf8')
                port = tr.select('div span:nth-of-type(2)')[0].get_text().encode('utf8')
                i = i + 1
                yield 'http://{}:{}'.format(ip.strip(), port.strip())

    def crawl_kuaidaili(self, pages=5):
        start_url = 'http://www.kuaidaili.com/free/inha/{}/'
        for page in xrange(1, pages+1):
            html = get_page(start_url.format(page))
            if html:
                bs = BeautifulSoup(html, 'lxml')
                iptrs = bs.select('#list > table > tbody > tr')
                for tr in iptrs:
                    proto = tr.select('td:nth-of-type(4)')[0].get_text().encode('utf8').lower()
                    ip = tr.select('td:nth-of-type(1)')[0].get_text().encode('utf8')
                    port = tr.select('td:nth-of-type(2)')[0].get_text().encode('utf8')
                    yield '{}://{}:{}'.format(proto, ip, port)
            sleep(30)

    def crawl_getproxyjp(self, pages=1):
        start_url = 'http://www.getproxy.jp/en/china/{}'
        for page in xrange(1, pages+1):
            html = get_page(start_url.format(page))
            if html:
                bs = BeautifulSoup(html, 'lxml')
                i = 0
                iptrs = bs.select('#mytable > tbody > tr')
                for tr in iptrs:
                    if i == 0:
                        i = i + 1
                        continue
                    proto = tr.select('td:nth-of-type(7)')[0].get_text().encode('utf8').lower()
                    ip_port = tr.select('td:nth-of-type(1)')[0].get_text().encode('utf8')
                    i = i + 1
                    yield '{}://{}'.format(proto, ip-port)
            sleep(30)

    def crawl_cnproxy(self):
        start_url = 'http://cn-proxy.com/'
        html = get_page(start_url)
        if html:
            bs = BeautifulSoup(html, 'lxml')
            iptrs = bs.select('#tablekit-table-22 > tbody > tr')
            for tr in iptrs:
                ip = tr.select('td:nth-of-type(1)')[0].get_text().encode('utf8')
                port = tr.select('td:nth-of-type(2)')[0].get_text().encode('utf8')
                yield 'http://{}:{}'.format(ip.strip(), port.strip())

if __name__ == '__main__':
    ps = ProxySpider()
    print ps.get_raw_proxies('crawl_cnproxy')
