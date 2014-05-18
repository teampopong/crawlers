from __future__ import unicode_literals
import re
from urlparse import urljoin

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.utils.url import url_query_parameter

from local.settings import DATA_DIR
from local.utils import tostr, save_file


__all__ = ['SeoulLocalAssemblySpider']


date_re = re.compile(r'(?P<date>\d{4}[\.-]\d{1,2}[\.-]\d{1,2})')
minutes_re = re.compile(r"window.open\('(?P<url>[^']+)'")
minute_filepath_fmt = '{DATA_DIR}/{daesu}/{date}/{filename}'


class SeoulLocalAssemblySpider(Spider):
    name = 'seoul-assembly'
    allowed_domains = ['ems.smc.seoul.kr']
    headers = {
        'Referer': 'http://ems.smc.seoul.kr/'
    }
    start_url = 'http://ems.smc.seoul.kr/source/Minute/simple/simple1.html?tag=lth'

    def start_requests(self):
        return [Request(url=self.start_url,
                        headers=self.headers,
                        callback=self.parse_list)]

    def parse_list(self, response):
        sel = Selector(response)
        links = sel.xpath("//table[@width='90%']//td/a")
        for link in links:
            yield self.request_from_link(response, link)


    def request_from_link(self, response, link):
        url = tostr(link.xpath('./@href'))

        if url.startswith('javascript'):
            return self.request_minutes(response, link)

        url = urljoin(response.url, url)
        return Request(url=url,
                      headers=self.headers,
                      callback=self.parse_list)

    def request_minutes(self, response, link):
        onclick = tostr(link.xpath('./@onclick'))

        m = minutes_re.match(onclick)
        if not m:
            raise UrlParseError(onclick)

        url = m.group('url')
        url = url.replace('frame.php', 'viewer.total.php')
        url = urljoin(response.url, url)

        return Request(url=url,
                      headers=self.headers,
                      callback=self.parse_minutes)

    def parse_minutes(self, response):
        filename = url_query_parameter(response.url, 'hfile')
        daesu = url_query_parameter(response.url, 'daesu')
        date = self.parse_date(response)
        save_file(minute_filepath_fmt.format(DATA_DIR=DATA_DIR, **locals()),
                  response.body)

    def parse_date(self, response):
        sel = Selector(response)
        title = tostr(sel.xpath('//title/text()'))
        m = date_re.search(title)
        if not m:
            raise DateParseError(title)
        date = m.group('date').replace('.', '-')
        return date


class DateParseError(Exception):
    pass


class UrlParseError(Exception):
    pass

