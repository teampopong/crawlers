#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from base import *
from utils import sanitize

class ElectedCrawler(SinglePageCrawler):

    _url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&electionType=4&electionCode=3&cityCode=-1&townCode=-1'

    format_suffix = '&statementId=%s&oldElectionType=%d&electionName=%s'

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
        return url

    def __init__(self, nth):
        self.nth = nth

Crawler = ElectedCrawler
