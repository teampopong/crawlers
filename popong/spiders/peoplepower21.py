# coding: utf-8

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
            yield Request(urls.special % id, callback=self.parse_special)
            yield Request(urls.attend % id, callback=self.parse_attend)

    def parse_private(self, response):
        id = extract_url(response.url, 'member_seq')
        hxs = HtmlXPathSelector(response)
        birth = extract(hxs, xpaths.private_birth_xpath)
        military = extract_text(hxs, xpaths.private_military_xpath)
        yield items.PrivateItem(type='private', id=id, birth=birth, military=military)

    def parse_special(self, response):
        id = extract_url(response.url, 'member_seq')
        hxs = HtmlXPathSelector(response)
        table_xpath = xpaths.special_table_xpath
        table_count = len(hxs.select(table_xpath + '/tr[td/table]'))
        if table_count == 1:
            party_xpath = table_xpath + '/tr[td/table][1]/td/table'
            election = []
            party = extract_table(hxs, party_xpath)
        elif table_count == 2:
            election_xpath = table_xpath + '/tr[td/table][1]/td/table'
            party_xpath = table_xpath + '/tr[td/table][2]/td/table'
            election = extract_table(hxs, election_xpath)
            party = extract_table(hxs, party_xpath)
        else:
            raise Exception("shouldn't happen")
        yield items.SpecialItem(type='special', id=id, election=election, party=party)

    def parse_attend(self, response):
        id = extract_url(response.url, 'member_seq')
        hxs = HtmlXPathSelector(response)
        yield Request(urls.attend_page % (id, 1), callback=self.parse_attend_page)
        pages = extract_ids(hxs, 'page')
        for page in pages:
            yield Request(urls.attend_page % (id, page), callback=self.parse_attend_page)

    def parse_attend_page(self, response):
        id = extract_url(response.url, 'member_seq')
        hxs = HtmlXPathSelector(response)
        table_xpath = xpaths.attend_table_xpath
        table_count = len(hxs.select(table_xpath + '/tr[td/table]'))
        assert table_count == 1
        attend_xpath = table_xpath + '/tr[td/table][1]/td/table'
        for attend in extract_table(hxs, attend_xpath):
            date = attend[u'회의날짜']
            meeting = attend[u'회차']
            status = attend[u'출석부']
            yield items.AttendItem(type='attend', id=id, date=date, meeting=meeting, status=status)
