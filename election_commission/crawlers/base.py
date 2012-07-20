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

    def parse(self, url, city_name=None):
        elems = get_xpath(url, '//td')
        num_attrs = len(self.attrs)
        members = (dict(zip(self.attrs, elems[i*num_attrs:(i+1)*num_attrs]))\
                    for i in xrange(len(elems) / num_attrs))

        members = [self.parse_member(member, city_name=city_name) for member in members]
        print 'crawled #%d - %s(%d)...' % (self.target, city_name or '비례대표', len(members))
        return members

    def parse_record(self, record):
        for attr in self.attrs:
            if attr not in self.attrs_exclude_parse_cell:
                record[attr] = parse_cell(record[attr])

    def parse_member(self, member, city_name=None):
        self.parse_record(member)

        # never change the order
        member['assembly_no'] = self.target
        member['elected'] = self.__class__.__name__.startswith('Elected')
        self.parse_member_image(member)
        self.parse_member_name(member)
        self.parse_member_birth(member)
        self.parse_member_district(member, city_name)
        self.parse_member_vote(member)

        return member

    def parse_member_image(self, member):
        if 'image' not in member: return

        rel_path = member['image'].find("./input[@type='image']").attrib['src']
        member['image'] = urljoin(self.url_image_base, rel_path)

    def parse_member_name(self, member):
        if 'name' not in member: return

        member['name_kr'], member['name_cn'] = map(sanitize, member['name'][:2])
        del member['name']

    def parse_member_birth(self, member):
        if 'birth' not in member: return

        member['birthyear'], member['birthmonth'], member['birthday'] =\
                split(member['birth'][0])
        del member['birth']

    def parse_member_district(self, member, city_name):
        if city_name:
            member['district'] = '%s %s' % (city_name, member['district'])

    def parse_member_vote(self, member):
        if 'vote' not in member: return
        member['votenum'], member['voterate'] = map(sanitize, member['vote'][:2])
        member['votenum'] = member['votenum'].replace(',', '')
        del member['vote']

class MultiCityCrawler(BaseCrawler):

    def city_codes(self):
        list_ = get_json(self.url_city_codes_json)['body']
        return map(lambda x: (x['CODE'], x['NAME']), list_)

    def url_list(self, city_code):
        return self.url_list_base + str(city_code)

    def crawl(self):
        # 지역구 대표
        jobs = []
        for city_code, city_name in self.city_codes():
            req_url = self.url_list(city_code)
            job = gevent.spawn(self.parse, req_url, city_name)
            jobs.append(job)
        gevent.joinall(jobs)
        people = flatten(job.get() for job in jobs)

        # 비례대표
        if hasattr(self, 'prop_crawler'):
            prop_people = self.prop_crawler.crawl()
            for person in prop_people:
                person['district'] = '비례대표'
            people.extend(prop_people)

        return people

class SinglePageCrawler(BaseCrawler):

    def crawl(self):
        people = self.parse(self.url_list)
        return people
