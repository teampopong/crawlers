#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from base import *
from utils import sanitize

class ElectedCrawler(SinglePageCrawler):

    _url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fep%2Fepei01.jsp'\
            '&electionType=1&cityCode=-1&proportionalRepresentationCode=-1'\
            '&electionCode=1&townCode=-1'

    format_suffix = '&statementId=%s&oldElectionType=%d&electionName=%s'

    args = {
            1: ('EPEI01_%2399', 0, '19480720'),
            2: ('EPEI01_%2399', 0, '19520805'),
            3: ('EPEI01_%2399', 0, '19560515'),
            4: ('EPEI01_%2399', 0, '19600315'),
            5: ('EPEI01_%2399', 0, '19631015'),
            6: ('EPEI01_%2399', 0, '19670503'),
            7: ('EPEI01_%2399', 0, '19710427'),
            8: ('EPEI01_%2399', 0, '19721223'),
            9: ('EPEI01_%2399', 0, '19780706'),
            10: ('EPEI01_%2399', 0, '19791206'),
            11: ('EPEI01_%2399', 0, '19800827'),
            12: ('EPEI01_%2399', 0, '19810225'),
            13: ('EPEI01_%2399', 0, '19871216'),
            14: ('EPEI01_%2399', 0, '19921218'),
            15: ('EPEI01_%2399', 0, '19971218'),
            16: ('EPEI01_%2399', 0, '20021219'),
            17: ('EPEI01_%231', 1, '20071219')
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
