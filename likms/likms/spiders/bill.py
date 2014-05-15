from __future__ import unicode_literals
from datetime import date
import re

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider

from likms.items import BillHtmlItem
from likms.rules import likms_url, XPATHS
from likms.utils import sel_to_str


__all__ = ['NewBillSpider']


ALL = 150
word_re = re.compile(r'\w+')


class NewBillSpider(Spider):
    name = 'new-bills'
    allowed_domains = ['likms.assembly.go.kr']
    headers = {
        'Referer': 'http://likms.assembly.go.kr'
    }

    def __init__(self, *args, **kwargs):
        super(NewBillSpider, self).__init__(*args, **kwargs)
        self.date_since = kwargs.get('date_since')

    def start_requests(self):
        date_since = self.date_since or date.today().isoformat()
        return [Request(url=likms_url('new-bill-list',
                                      date_since=date_since,
                                      size=ALL),
                        headers=self.headers,
                        callback=self.parse_new_bills)]

    def parse_new_bills(self, response):
        sel = Selector(response)
        bills_sel = sel.xpath(XPATHS['new-bill-list'])
        bill_id_pairs = (self.parse_new_bill_id_pair(bill_sel)
                         for bill_sel in bills_sel)
        bill_id_pairs = filter(None, bill_id_pairs)
        for bill_id, link_id in bill_id_pairs:
            yield self.bill_request(bill_id, link_id)

    def parse_new_bill_id_pair(self, sel):
        columns = sel.xpath(XPATHS['columns'])
        if len(columns) != 8:
            return

        bill_id = sel_to_str(columns[0].xpath('text()'))
        link_id = word_re.findall(columns[1].xpath('a/@href').extract()[0])[2]
        return bill_id, link_id

    def bill_request(self, bill_id, link_id):
        '''This is composed of 4 sequential page request'''
        meta = {
            'bill_id': bill_id,
            'link_id': link_id,
        }
        return Request(url=likms_url('bill', link_id=link_id),
                       headers=self.headers,
                       meta=meta,
                       callback=self.parse_bill)

    def parse_bill(self, response):
        bill_id, link_id = [response.meta[k] for k in ('bill_id', 'link_id')]
        yield BillHtmlItem(bill_id, body=response.body)
        # yield self.summary_request(bill_id=bill_id,
        #                            link_id=link_id)

    def summary_request(self, bill_id, link_id):
        pass

