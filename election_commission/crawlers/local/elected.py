#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from base import *
from utils import sanitize
from static import get_election_type_id, url_city_ids_json

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

    attrs = ['district', 'party', 'name', 'sex', 'birth', 'job', 'education',
            'experience', 'vote']

    @property
    def url_list(self):
        url = self._url_list_base + self.format_suffix % self.args[self.nth]
        url += self.election_suffix % get_election_type_id(self.level)
        print url
        return url

    @property
    def url_city_ids_json(self):
        json = url_city_ids_json(self.nth, self.level)
        print json
        return json

    def __init__(self, nth, level):
        self.nth = nth
        self.level = level

Crawler = ElectedCrawler
