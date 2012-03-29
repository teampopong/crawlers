#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from urlparse import urljoin
import re

from utils import get_json, get_xpath, stringify

class BaseCrawler(object):
    url_image_base = 'http://info.nec.go.kr'

    attrs = []
    attrs_exclude_stringify = ['name', 'image']

    regex_split = re.compile('[/\(\)]')
    regex_join = re.compile('\s')

    def split(self, txt):
        splitted = self.regex_split.split(txt)
        concatenated = [self.regex_join.sub('', s) for s in splitted]
        return concatenated

    def parse_cand_page(self, url):
        elems = get_xpath(url, '//td')
        num_attrs = len(self.attrs)
        members = (dict(zip(self.attrs, elems[i*num_attrs:(i+1)*num_attrs]))\
                    for i in xrange(len(elems) / num_attrs))

        members = [self.parse_member(member) for member in members]
        return members

    def stringify_member_attrs(self, member):
        for attr in self.attrs:
            if attr not in self.attrs_exclude_stringify:
                member[attr] = stringify(member[attr]).strip()

    def parse_member(self, member):
        self.stringify_member_attrs(member)

        # never change the order
        self.parse_member_image(member)
        self.parse_member_name(member)
        self.parse_member_birth(member)
        self.parse_member_experience(member)

        return member

    def parse_member_image(self, member):
        if 'image' not in member: return

        rel_path = member['image'].find("./input[@type='image']").attrib['src']
        member['image'] = urljoin(self.url_image_base, rel_path)

    def parse_member_name(self, member):
        if 'name' not in member: return

        txt = stringify(member['name']).strip()
        member['name_kr'], member['name_cn'] = self.split(txt)[:2]
        member['name'] = member['name_kr']

    def parse_member_birth(self, member):
        if 'birth' not in member: return

        member['birthyear'], member['birthmonth'], member['birthday'] =\
                self.split(member['birth'])[:3]
        del member['birth']

    def parse_member_experience(self, member):
        if 'experience' not in member: return

        pass # TODO: 이거 구현하면 parse_member도 고쳐야 함

class MultiCityCrawler(BaseCrawler):

    def city_codes(self):
        list_ = get_json(self.url_city_codes_json)['body']
        return map(lambda x: (x['CODE'], x['NAME']), list_)

    def url_cand_list(self, city_code):
        return self.url_cand_list_base + str(city_code)

    def crawl(self, target):
        cand_list = []
        for city_code, city_name in self.city_codes():
            req_url = self.url_cand_list(city_code)
            dist_cand_list = self.parse_cand_page(req_url)
            cand_list.extend(dist_cand_list)
            print 'crawled %s(%d)...' % (city_name, len(dist_cand_list))

        if hasattr(self, 'prop_crawler'):
            prop_cand_list = self.prop_crawler.crawl(target)
            cand_list.extend(prop_cand_list)
            print 'crawled 비례대표(%d)...' % (len(prop_cand_list),)

        return cand_list

class SinglePageCrawler(BaseCrawler):

    def crawl(self, target):
        cand_list = self.parse_cand_page(self.url_cand_list)
        return cand_list

class CrawlerUntil16(BaseCrawler):

    election_names = [None, '19480510', '19500530', '19540520', '19580502',
            '19600729', '19631126', '19670608', '19710525', '19730227',
            '19781212', '19810325', '19850212', '19880426', '19920324',
            '19960411', '20000413']

    url_cand_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&statementId=CPRI03_%2300&oldElectionType=0&electionType=2'\
            '&electionCode=2&cityCode=0&proportionalRepresentationCode=-1'\
            '&sggCityCode=-1&townCode=-1&sggTownCode=0&dateCode=0'\
            '&electionName='

    attrs = ['district', 'cand_no', 'party', 'name', 'sex', 'birth',
             'job', 'education', 'experience']

    def crawl(self, target):
        url = self.url_cand_list + self.election_names[target]
        cand_list = self.parse_cand_page(url)
        return cand_list

class Crawler17(MultiCityCrawler):
    url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
            'selectbox_cityCodeBySgJson_GuOld.json?electionId=0000000000'\
            '&electionCode=20040415'

    url_cand_list_base = 'http://info.nec.go.kr/electioninfo/'\
            'electionInfo_report.xhtml?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&statementId=CPRI03_%2300&oldElectionType=0&electionType=2'\
            '&electionName=20040415&electionCode=2&sggCityCode=-1&townCode=-1'\
            '&sggTownCode=0&dateCode=0&cityCode='

    attrs = ['district', 'cand_no', 'party', 'name', 'sex', 'birth',
             'job', 'education', 'experience']

    def __init__(self):
        self.prop_crawler = Crawler17Proportional()

class Crawler18(MultiCityCrawler):
    url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
            'selectbox_cityCodeBySgJson_Old.json?electionId=0000000000'\
            '&subElectionCode=2&electionCode=20080409'

    url_cand_list_base = 'http://info.nec.go.kr/electioninfo/'\
            'electionInfo_report.xhtml?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&statementId=CPRI03_%231&oldElectionType=1&electionType=2'\
            '&electionName=20080409&electionCode=2&sggCityCode=-1&townCode=-1'\
            '&sggTownCode=0&dateCode=0&cityCode='

    attrs = ['district', 'cand_no', 'party', 'name', 'sex', 'birth',
             'job', 'education', 'experience']

    def __init__(self):
        self.prop_crawler = Crawler18Proportional()

class Crawler19(MultiCityCrawler):
    url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/'\
            'selectbox_cityCodeBySgJson.json?electionId=0020120411&electionCode=2'
    url_cand_list_base = 'http://info.nec.go.kr/electioninfo/'\
            'electionInfo_report.xhtml?electionId=0020120411'\
            '&requestURI=%2Felectioninfo%2F0020120411%2Fcp%2Fcpri03.jsp'\
            '&statementId=CPRI03_%232&electionCode=2&sggCityCode=0&cityCode='

    attrs = ['district', 'image', 'cand_no', 'party', 'name', 'sex',
             'birth', 'address', 'job', 'education', 'experience']

    def __init__(self):
        self.prop_crawler = Crawler19Proportional()

    def parse_member(self, member):
        member = super(Crawler19, self).parse_member(member)

        self.parse_member_pledge(member)

        return member

    def parse_member_pledge(self, member):
        pass # TODO: implement

class Crawler17Proportional(SinglePageCrawler):
    url_cand_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&statementId=CPRI03_%2300&oldElectionType=0&electionType=2'\
            '&electionName=20040415&electionCode=7&cityCode=-1'\
            '&proportionalRepresentationCode=0&sggCityCode=-1'\
            '&townCode=-1&sggTownCode=0&dateCode=0'

    attrs = ['cand_no', 'party', 'name', 'sex', 'birth', 'job', 'education',
             'experience']

    def parse_member(self, member):
        member = super(Crawler17Proportional, self).parse_member(member)
        member['district'] = '비례대표'

        return member

class Crawler18Proportional(SinglePageCrawler):
    url_cand_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&statementId=CPRI03_%231&oldElectionType=1&electionType=2'\
            '&electionName=20080409&electionCode=7'\
            '&proportionalRepresentationCode=0&dateCode=0'

    attrs = ['cand_no', 'party', 'name', 'sex', 'birth', 'job', 'education',
             'experience']

    def parse_member(self, member):
        member = super(Crawler18Proportional, self).parse_member(member)
        member['district'] = '비례대표'

        return member

class Crawler19Proportional(SinglePageCrawler):
    url_cand_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0020120411'\
            '&requestURI=%2Felectioninfo%2F0020120411%2Fcp%2Fcpri03.jsp'\
            '&statementId=CPRI03_%237&electionCode=7'

    attrs = ['district', 'image', 'party', 'cand_no', 'name', 'sex',
            'birth', 'address', 'job', 'education', 'experience']

    def parse_member(self, member):
        member = super(Crawler19Proportional, self).parse_member(member)

        self.parse_member_party(member)

        return member

    def parse_member_party(self, member):
        member['party'] = self.split(member['party'])[0]

