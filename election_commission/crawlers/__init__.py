#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import assembly
import local
import president
from utils import InvalidCrawlerError

def Crawler(target, _type, nth, level):
    if target == 'assembly':
        return assembly.Crawler(_type, nth)
    elif target == 'local':
        return local.Crawler(_type, nth, level)
    elif target == 'president':
        return president.Crawler(_type, nth)
    else:
        raise InvalidCrawlerError(target, _type, nth)
