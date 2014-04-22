#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from base import *
from urls import get_election_url_base
from static import get_election_type_id

def Crawler(nth, level):
    if nth==6:
        print level
        if level=='education_governor' or level=='education_member':
            crawler = PreCandEducationCrawler(nth, level)
        else:
            crawler = PreCandCrawler(nth, level)
    else:
        raise NotImplementedError('Precandidate crawler for 1-5th local')
    return crawler

class PreCandCrawler(MultiCityCrawler):
    _election_names = [None, '19950627', '19980604', '20020613', '20060531',
            '20100602', '20140604']

    attrs = ['district', 'party', 'image', 'name', 'sex', 'birth', 'address',
            'job', 'education', 'experience', 'regdate']

    @property
    def election_id(self):
        return int(self.nth)

    @property
    def election_name(self):
        return self._election_names[self.election_id]

    @property
    def url_city_ids_json(self):
        return 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json?electionId=0020140604&electionCode=%s' % get_election_type_id(self.level)

    @property
    def url_list_base(self):
        return get_election_url_base(self.election_name, self.level)\
                + '&cityCode='

    def __init__(self, nth, level):
        self.nth = nth
        self.level = level

class PreCandEducationCrawler(SinglePageCrawler):
    _election_names = [None, '19950627', '19980604', '20020613', '20060531',
            '20100602', '20140604']

    attrs = ['district', 'image', 'name', 'sex', 'birth', 'address',
            'job', 'education', 'experience', 'regdate']

    @property
    def election_id(self):
        return int(self.nth)

    @property
    def election_name(self):
        return self._election_names[self.election_id]

    @property
    def url_city_ids_json(self):
        return 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json?electionId=0020140604&electionCode=%s' % get_election_type_id(self.level)

    @property
    def url_list(self):
        return get_election_url_base(self.election_name, self.level)

    def __init__(self, nth, level):
        self.nth = nth
        self.level = level
