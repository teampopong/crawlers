#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import assembly
import mayor
import president
from utils import InvalidCrawlerError

def Crawler(target, _type, nth):
    if target == 'assembly':
        return assembly.Crawler(_type, nth)
    elif target == 'mayor':
        return mayor.Crawler(_type, nth)
    elif target == 'president':
        return president.Crawler(_type, nth)
    else:
        raise InvalidCrawlerError(target, _type, nth)
