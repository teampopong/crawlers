#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2
import gevent
from gevent import monkey; monkey.patch_all()

import utils
from settings import NUM_PAGES, END_BILL, DIR, BASEURL

def get_files(page, directory):
    try:
        url = BASEURL['list'] + 'PAGE=%d&PAGE_SIZE=%d' % (page, NUM_PAGES)
        fn = '%s/%s.html' % (directory, str(page))
        utils.get_webpage(url, fn)
        print fn
    except urllib2.URLError, e:
        print 'failed'

def check_files(directory):
    files = os.listdir(directory)
    nums = [int(f.strip('.html')) for f in files]
    return [m for m in range(1, END_BILL/NUM_PAGES) if m not in nums]

if __name__=='__main__':
    directory = DIR['list']
    utils.check_dir(directory)

    #FIXME: index
    jobs = [gevent.spawn(get_files, page, directory)\
            for page in range(1, END_BILL/NUM_PAGES+4)]
    gevent.joinall(jobs)

    missing = check_files(directory)
    print
    print missing
    while (missing != []):
        for m in missing:
            get_files(m, directory)
        missing = check_files(directory)
