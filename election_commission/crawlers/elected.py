#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from crawlers.base import *

def Crawler(target):
    if 1 <= target <= 6:
        crawler = ElectedCrawlerUntil6(target)
    elif target <= 16:
        crawler = ElectedCrawlerUntil16(target)
    elif target == 17:
        crawler = ElectedCrawler17()
    elif target == 18:
        crawler = ElectedCrawler18()
    else:
        raise InvalidCrawlerError('elected', target)
    return crawler

class ElectedCrawlerUntil16(MultiCityCrawler):
    _election_names = [None, '19480510', '19500530', '19540520', '19580502',
            '19600729', '19631126', '19670608', '19710525', '19730227',
            '19781212', '19810325', '19850212', '19880426', '19920324',
            '19960411', '20000413']

    _url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
            'selectbox_cityCodeBySgJson_GuOld.json?electionId=0000000000'\
            '&electionCode='

    _url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&statementId=EPEI01_%2399&oldElectionType=0&electionType=2'\
            '&electionCode=2&proportionalRepresentationCode=-1'\
            '&townCode=-1&electionName='

    attrs = ['district', 'party', 'name', 'sex', 'birth', 'job', 'education',
            'experience', 'vote']

    @property
    def election_name(self):
        return self._election_names[self.target]

    @property
    def url_city_codes_json(self):
        return self._url_city_codes_json + self.election_name

    @property
    def url_list_base(self):
        return self._url_list_base + self.election_name + '&cityCode='

    def __init__(self, target):
        self.target = target

class ElectedCrawlerUntil6(ElectedCrawlerUntil16):

    def parse_member_birth(self, member):
        if 'birth' not in member: return
        super(ElectedCrawlerUntil6, self).parse_member_birth(member)
        del member['birthmonth']
        del member['birthday']

class ElectedCrawler17(MultiCityCrawler):
    target = 17

    url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
            'selectbox_cityCodeBySgJson_GuOld.json?electionId=0000000000'\
            '&electionCode=20040415'

    url_list_base = 'http://info.nec.go.kr/electioninfo/'\
            'electionInfo_report.xhtml?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&statementId=EPEI01_%2399&oldElectionType=0&electionType=2'\
            '&electionName=20040415&electionCode=2&townCode=-1&cityCode='

    attrs = ['district', 'party', 'name', 'sex', 'birth', 'job', 'education',
             'experience', 'vote']

    def __init__(self):
        self.prop_crawler = ElectedCrawler17Proportional()

class ElectedCrawler18(MultiCityCrawler):
    target = 18

    url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
            'selectbox_cityCodeBySgJson_Old.json?electionId=0000000000'\
            '&subElectionCode=2&electionCode=20080409'

    url_list_base = 'http://info.nec.go.kr/electioninfo/'\
            'electionInfo_report.xhtml?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&statementId=EPEI01_%232&oldElectionType=1&electionType=2'\
            '&electionName=20080409&electionCode=2&cityCode='

    attrs = ['district', 'party', 'name', 'sex', 'birth', 'job', 'education',
             'experience', 'vote']

    def __init__(self):
        self.prop_crawler = ElectedCrawler18Proportional()

class ElectedCrawler17Proportional(SinglePageCrawler):
    target = 17

    url_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&statementId=EPEI01_%2399&oldElectionType=0&electionType=2'\
            '&electionName=20040415&electionCode=7'

    attrs = ['party', 'recommend_priority', 'name', 'sex', 'birth', 'job',
            'education', 'experience']

class ElectedCrawler18Proportional(SinglePageCrawler):
    target = 18

    url_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&statementId=EPEI01_%232&oldElectionType=1&electionType=2'\
            '&electionName=20080409&electionCode=7'

    attrs = ['party', 'recommend_priority', 'name', 'sex', 'birth', 'job',
            'education', 'experience']
