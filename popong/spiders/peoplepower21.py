import re
import lxml.html

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request

from .. import items
from . import urls
from . import xpaths

def convert_to_text(e):
    texts = []
    texts.append(e.text.strip())
    for br in e:
        assert br.tag == 'br'
        texts.append('\n')
        if e.tail: texts.append(e.tail.strip())
    return ''.join(texts)

def extract(hxs, xpath):
    result = hxs.select(xpath).extract()
    if not result: return ''
    return result[0]

def extract_text(hxs, xpath):
    result = hxs.select(xpath).extract()
    if not result: return ''
    return convert_to_text(lxml.html.fromstring(result[0]))

def extract_ids(hxs, key):
    xpath = '//a[contains(@href, "%s=")]/@href' % key
    return hxs.select(xpath).re(r'%s=(\d+)' % key)

def extract_texts(hxs, key):
    xpath = '//a[contains(@href, "%s=")]/text()' % key
    return hxs.select(xpath).extract()

def extract_url(url, key):
    return re.search(r'%s=(\d+)' % key, url).group(1)

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
