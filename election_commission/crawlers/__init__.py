#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import assembly
from utils import InvalidCrawlerError

def Crawler(target, _type, nth):
    if target == 'assembly':
        return assembly.Crawler(_type, nth)
    else:
        raise InvalidCrawlerError(target, _type, nth)
