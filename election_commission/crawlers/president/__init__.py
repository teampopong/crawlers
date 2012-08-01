#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import candidates
from utils import InvalidCrawlerError

def Crawler(_type, nth):
    if _type == 'candidates':
        return candidates.Crawler(nth)
    else:
        raise InvalidCrawlerError('president', _type, nth)
