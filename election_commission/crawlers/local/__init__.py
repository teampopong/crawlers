#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import candidates
import elected
import precandidates
from utils import InvalidCrawlerError

def Crawler(_type, nth, level):
    if _type == 'candidates':
        return candidates.Crawler(nth, level)
    elif _type == 'elected':
        return elected.Crawler(nth, level)
    elif _type == 'precandidates':
        return precandidates.Crawler(nth, level)
    else:
        raise InvalidCrawlerError('local', _type, nth, level)
