#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2
import gevent
from gevent import monkey; monkey.patch_all()

import utils
from settings import NUM_PAGES, END_BILL, DIR, LIST_DATA, BASEURL

def get_files(page):
    try:
        url = BASEURL['list'] + 'PAGE=%d&PAGE_SIZE=%d' % (page, NUM_PAGES)
        fn = '%s/%s.html' % (DIR['list'], str(page))
        utils.get_webpage(url, fn)
        print page
    except urllib2.URLError, e:
        print 'failed'

def check_files(directory):
    files = os.listdir(directory)
    nums = [int(f.strip('.html')) for f in files]
    return [m for m in range(1, END_BILL/NUM_PAGES) if m not in nums]

if __name__=='__main__':
    if not os.path.exists(DIR['list']):
        os.makedirs(DIR['list'])

    #FIXME: index
    jobs = [gevent.spawn(get_files, page)\
            for page in range(1, END_BILL/NUM_PAGES+4)]
    gevent.joinall(jobs)

    missing = check_files(DIR['list'])
    print
    print missing
    while (missing != []):
        for m in missing:
            get_files(m)
        missing = check_files(DIR['list'])
