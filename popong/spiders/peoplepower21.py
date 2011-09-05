from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request

from .. import items
from . import urls
from . import xpaths
from .utils import *

class Peoplepower21Spider(BaseSpider):
    name = 'peoplepower21'

    def start_requests(self):
        yield Request(urls.start, method='POST')

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        ids = extract_ids(hxs, 'member_seq')
        names = extract_texts(hxs, 'member_seq')
        for id, name in zip(ids, names):
            yield items.MemberItem(type='member', id=id, name=name)
            yield Request(urls.private % id, callback=self.parse_private)

    def parse_private(self, response):
        id = extract_url(response.url, 'member_seq')
        hxs = HtmlXPathSelector(response)
        birth = extract(hxs, xpaths.private_birth_xpath)
        military = extract_text(hxs, xpaths.private_military_xpath)
        yield items.PrivateItem(type='private', id=id, birth=birth, military=military)
