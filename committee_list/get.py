#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os

from crawlers import committee_list
from settings import BASEURL, DIR

def get(target):

    directory = '%s/%s' % (DIR['html'], target)
    baseurl = BASEURL[target]
    filename = '%s/%s.csv' % (DIR['results'], target)

    if not os.path.exists(directory):
        os.makedirs(directory)

    eval('%s.crawl("%s", "%s")' % (target, baseurl, directory))
    eval('%s.parse("%s", "%s")' % (target, directory, filename))

if __name__=='__main__':
    get('committee_list')
