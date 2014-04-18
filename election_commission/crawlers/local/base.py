#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import gevent
from gevent import monkey
import itertools
from urlparse import urljoin

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split

monkey.patch_all()

class BaseCrawler(object):
    url_image_base = 'http://info.nec.go.kr'

    attrs = []
    attrs_exclude_parse_cell = ['image']

    def parse(self, url):
        elems = get_xpath(url, '//td')
        num_attrs = len(self.attrs)
        members = (dict(zip(self.attrs, elems[i*num_attrs:(i+1)*num_attrs]))\
                    for i in xrange(len(elems) / num_attrs))

        members = [self.parse_member(member) for member in members]
        print 'crawled #%d (%d)...' % (self.nth, len(members))
        return members

    def parse_record(self, record):
        for attr in self.attrs:
            if attr not in self.attrs_exclude_parse_cell:
                record[attr] = parse_cell(record[attr])

    def parse_member(self, member):
        self.parse_record(member)

        # never change the order
        member['gov_no'] = self.nth
        member['elected'] = self.__class__.__name__.startswith('Elected')
        self.parse_member_name(member)
        self.parse_member_birth(member)
        self.parse_member_vote(member)

        return member

    def parse_member_name(self, member):
        if 'name' not in member: return

        member['name_kr'], member['name_cn'] = map(sanitize, member['name'][:2])
        del member['name']

    def parse_member_birth(self, member):
        if 'birth' not in member: return

        member['birthyear'], member['birthmonth'], member['birthday'] =\
                split(member['birth'][0])
        del member['birth']

    def parse_member_vote(self, member):
        if 'vote' not in member: return
        member['votenum'], member['voterate'] = map(sanitize, member['vote'][:2])
        member['votenum'] = member['votenum'].replace(',', '')
        del member['vote']

class SinglePageCrawler(BaseCrawler):

    def crawl(self):
        people = self.parse(self.url_list)
        return people
