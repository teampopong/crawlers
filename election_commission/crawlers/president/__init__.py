#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import candidates
import elected
from utils import InvalidCrawlerError

def Crawler(_type, nth):
    if _type == 'candidates':
        return candidates.Crawler(nth)
    elif _type == 'elected':
        return elected.Crawler(nth)
    elif _type == 'precandidates':
        raise NotImplementedError('President precandidate crawler')
    else:
        raise InvalidCrawlerError('president', _type, nth)
