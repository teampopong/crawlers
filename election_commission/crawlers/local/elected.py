#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from base import *
from utils import sanitize
from static import get_election_id, get_election_type_id, get_valid_election_type_ids
from static import reversed_election_types, url_city_ids_json

def Crawler(nth, level):
    print level

    election_id = get_election_id(nth)
    valid_election_type_ids = get_valid_election_type_ids(election_id)
    if get_election_type_id(level) not in valid_election_type_ids:
        type_names = [reversed_election_types[t]\
                for t in valid_election_type_ids]
        raise Exception('Not valid election type for this election_id: %s'\
                % ','.join(type_names))

    if level in ['province_governor', 'province_proportional']:
        crawler = ElectedCrawler(nth, level)
    else:
        crawler = OtherElectedCrawler(nth, level)
    return crawler

class ElectedCrawler(SinglePageCrawler):
    _url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&electionType=4&cityCode=-1&townCode=-1'

    format_suffix = '&statementId=%s&oldElectionType=%d&electionName=%s'
    election_suffix = '&electionCode=%s'

    args = {
            1: ('EPEI01_%2399', 0, '19950627'),
            2: ('EPEI01_%2399', 0, '19980604'),
            3: ('EPEI01_%2399', 0, '20020613'),
            4: ('EPEI01_%233', 1, '20060531'),
            5: ('EPEI01_%233', 1, '20100602')
            }

    @property
    def attrs(self):
        if self.level in ['province_member', 'municipality_member']:
            return ['region', 'district', 'party', 'name', 'sex', 'birth',\
                    'job', 'education', 'experience', 'vote']
        elif self.level.endswith('proportional'):
            return ['district', 'party', 'rank', 'name', 'sex', 'birth',\
                    'job', 'education', 'experience']
        else:
            return ['district', 'party', 'name', 'sex', 'birth', 'job',\
                    'education', 'experience', 'vote']

    @property
    def url_list(self):
        url = self._url_list_base + self.format_suffix % self.args[self.nth]
        url += self.election_suffix % get_election_type_id(self.level)
        return url

    @property
    def url_city_ids_json(self):
        json = url_city_ids_json(self.nth, self.level)
        return json

    def __init__(self, nth, level):
        self.nth = nth
        self.level = level


class OtherElectedCrawler(MultiCityCrawler):
    _url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&electionType=4&townCode=-1'

    format_suffix = '&statementId=%s&oldElectionType=%d&electionName=%s'
    election_suffix = '&electionCode=%s'

    args = {
            1: ('EPEI01_%2399', 0, '19950627'),
            2: ('EPEI01_%2399', 0, '19980604'),
            3: ('EPEI01_%2399', 0, '20020613'),
            4: ('EPEI01_%234', 1, '20060531'),
            5: ('EPEI01_%235', 1, '20100602')
            }

    @property
    def attrs(self):
        if self.level in ['province_member', 'municipality_member']:
            return ['region', 'district', 'party', 'name', 'sex', 'birth',\
                    'job', 'education', 'experience', 'vote']
        elif self.level.endswith('proportional'):
            return ['district', 'party', 'rank', 'name', 'sex', 'birth',\
                    'job', 'education', 'experience']
        elif self.level.startswith('education'):
            return ['district', 'name', 'sex', 'birth', 'job', 'education',\
                    'experience', 'vote']
        else:
            return ['district', 'party', 'name', 'sex', 'birth', 'job',\
                    'education', 'experience', 'vote']

    @property
    def url_list_base(self):
        url = self._url_list_base + self.format_suffix % self.args[self.nth]
        url += self.election_suffix % get_election_type_id(self.level)
        url += '&cityCode='
        return url

    @property
    def url_city_ids_json(self):
        json = url_city_ids_json(self.nth, self.level)
        return json

    def __init__(self, nth, level):
        self.nth = nth
        self.level = level
