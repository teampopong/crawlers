#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from base import *
from static import get_election_id, get_election_type_id, get_valid_election_type_ids
from static import url_city_ids_json as ucij
from static import reversed_election_types

def Crawler(nth, level):
    print level
    election_id = get_election_id(nth)
    valid_election_type_ids = get_valid_election_type_ids(election_id)
    if get_election_type_id(level) not in valid_election_type_ids:
        type_names = [reversed_election_types[t]\
                for t in valid_election_type_ids]
        raise Exception('Not valid election type for this election_id: %s'\
                % ','.join(type_names))
    if level in ['province_governor', 'education_governor']:
        crawler = CandCrawler(nth, level)
    else:
        crawler = OtherCandCrawler(nth, level)
    return crawler

class CandCrawler(SinglePageCrawler):

    _url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&electionType=4&cityCode=0&sggCityCode=-1'\
            '&townCode=-1&sggTownCode=0&dateCode=0'

    format_suffix = '&statementId=%s&oldElectionType=%d&electionName=%s'
    election_suffix = '&electionCode=%s'

    args = {
            1: ('CPRI03_%2300', 0, '19950627'),
            2: ('CPRI03_%2300', 0, '19980604'),
            3: ('CPRI03_%2300', 0, '20020613'),
            4: ('CPRI03_%231', 1, '20060531'),
            5: ('CPRI03_%231', 1, '20100602')
            }

    @property
    def attrs(self):
        if self.level=='education_governor':
            attrs = ['district', 'name', 'sex', 'birth', 'job', 'education',
                    'experience']
        else:
            attrs = ['district', 'candno', 'party', 'name', 'sex', 'birth', 'job',
                'education', 'experience']
        return attrs

    @property
    def url_city_ids_json(self):
        return 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json?electionId=0000000000&electionCode=%s' % get_election_id(self.nth)

    @property
    def url_list(self):
        url = self._url_list_base + self.format_suffix % self.args[self.nth]
        url += self.election_suffix % get_election_type_id(self.level)
        print url
        return url

    def __init__(self, nth, level):
        self.nth = nth
        self.level = level

class OtherCandCrawler(MultiCityCrawler):

    _url_list_base= 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&electionType=4&townCode=0&sggTownCode=0&sggCityCode=-1&dateCode=0'

    format_suffix = '&statementId=%s&oldElectionType=%d&electionName=%s'
    election_suffix = '&electionCode=%s'

    args = {
            1: ('CPRI03_%2300', 0, '19950627'),
            2: ('CPRI03_%2300', 0, '19980604'),
            3: ('CPRI03_%2300', 0, '20020613'),
            4: ('CPRI03_%231', 1, '20060531'),
            5: ('CPRI03_%231', 1, '20100602')
            }

    @property
    def attrs(self):
        if self.level=='education_member':
            attrs = ['district', 'name', 'sex', 'birth', 'job', 'education',
                    'experience']
        elif self.level.endswith('proportional'):
            attrs = ['district', 'party', 'rank', 'name', 'sex', 'birth',
                    'job', 'education', 'experience']
        else:
            attrs = ['district', 'candno', 'party', 'name', 'sex', 'birth', 'job',
                'education', 'experience']
        return attrs

    @property
    def url_city_ids_json(self):
        return ucij(self.nth, self.level)

    @property
    def url_list_base(self):
        url = self._url_list_base + self.format_suffix % self.args[self.nth]
        url += self.election_suffix % get_election_type_id(self.level)
        url += '&cityCode='
        return url

    def __init__(self, nth, level):
        self.nth = nth
        self.level = level
