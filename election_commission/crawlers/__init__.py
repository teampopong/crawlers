#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import crawlers.candidates as candidates
import crawlers.elected as elected
from utils import InvalidCrawlerError

def Crawler(_type, target):
    if _type == 'candidates':
        return candidates.Crawler(target)
    elif _type == 'elected':
        return elected.Crawler(target)
    else:
        raise InvalidCrawlerError(_type, target)
