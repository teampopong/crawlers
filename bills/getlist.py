#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2
import gevent
from gevent import monkey; monkey.patch_all()

import utils
from settings import BASEURL, DIR, END_BILL, LIST_NPAGES, PAGE_SIZE

def get_files(page, directory):
    try:
        url = BASEURL['list'] + 'PAGE=%d&PAGE_SIZE=%d' % (page, PAGE_SIZE)
        fn = '%s/%d.html' % (directory, LIST_NPAGES-page+1)
        utils.get_webpage(url, fn)
        print fn
    except urllib2.URLError, e:
        print 'failed'

def check_files(directory):
    files = os.listdir(directory)
    nums = [int(f.strip('.html')) for f in files]
    return [m for m in range(1, LIST_NPAGES+1) if m not in nums]

if __name__=='__main__':
    directory = DIR['list']
    utils.check_dir(directory)

    jobs = [gevent.spawn(get_files, page, directory)\
            for page in range(1, LIST_NPAGES+1)]
    gevent.joinall(jobs)

    '''
    missing = check_files(directory)
    print
    print missing
    while (missing != []):
        for m in missing:
            get_files(m, directory)
        missing = check_files(directory)

    get_files(103, directory)
    '''
