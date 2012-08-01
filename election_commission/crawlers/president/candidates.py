#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from base import *
from utils import sanitize

class CandCrawler(SinglePageCrawler):
    _url_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'\
            '?electionId=0000000000'\
            '&requestURI=%2Felectioninfo%2F0000000000%2Fcp%2Fcpri03.jsp'\
            '&electionType=1&cityCode=-1&proportionalRepresentationCode=-1'\
            '&sggCityCode=-1&townCode=-1&sggTownCode=0&electionCode=1&dateCode=0'

    format_suffix = '&statementId=%s&oldElectionType=%d&electionName=%s'

    args = {
            1: ('CPRI03_%2300', 0, '19480720'),
            2: ('CPRI03_%2300', 0, '19520805'),
            3: ('CPRI03_%2300', 0, '19560515'),
            4: ('CPRI03_%2300', 0, '19600315'),
            5: ('CPRI03_%2300', 0, '19631015'),
            6: ('CPRI03_%2300', 0, '19670503'),
            7: ('CPRI03_%2300', 0, '19710427'),
            8: ('CPRI03_%2300', 0, '19721223'),
            9: ('CPRI03_%2300', 0, '19780706'),
            10: ('CPRI03_%2300', 0, '19791206'),
            11: ('CPRI03_%2300', 0, '19800827'),
            12: ('CPRI03_%2300', 0, '19810225'),
            13: ('CPRI03_%2300', 0, '19871216'),
            14: ('CPRI03_%2300', 0, '19921218'),
            15: ('CPRI03_%2300', 0, '19971218'),
            16: ('CPRI03_%2300', 0, '20021219'),
            17: ('CPRI03_%231', 1, '20071219')
            }

    attrs = ['district', 'candno', 'party', 'name', 'sex', 'birth', 'job',
            'education', 'experience']

    @property
    def url_list(self):
        url = self._url_list_base + self.format_suffix % self.args[self.nth]
        return url

    def __init__(self, nth):
        self.nth = nth

Crawler = CandCrawler
