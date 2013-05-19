#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re
import math
import urllib2
import gevent
from gevent import monkey; monkey.patch_all()

import utils
from settings import BASEURL, DIR, END_BILL, PAGE_SIZE

def get_files(page, directory, npages):
    try:
        url = BASEURL['list'] + 'PAGE=%d&PAGE_SIZE=%d' % (page, PAGE_SIZE)
        pn = npages - page + 1
        fn = '%s/%d.html' % (directory, pn)
        utils.get_webpage(url, fn)
        print 'Got %s.html' % pn
    except (urllib2.URLError, IOError) as e:
        print 'Failed to get %s due to %s' % (fn, e.__repr__)

def get_npages(directory):
    fn = '%s/tmp.html' % directory
    utils.get_webpage(BASEURL['list'], fn)
    page = utils.read_webpage(fn)
    m = re.search(u'총(.+)건', page.xpath('//span[@class="text3"]/text()')[0])
    nbills = int(m.group(1))
    npages = int(math.ceil(nbills/float(PAGE_SIZE)))
    return nbills, npages

def check_files(directory, npages):
    files = os.listdir(directory)
    nums = [int(f.strip('.html')) for f in files]
    return [m for m in range(1, npages+1) if m not in nums]

def getlist():
    directory = DIR['list']
    utils.check_dir(directory)

    nbills, npages = get_npages(directory)
    print 'Total %d bills, %d pages to %s' % (nbills, npages, directory)

    jobs = [gevent.spawn(get_files, page, directory, npages)\
            for page in range(1, npages+1)]
    gevent.joinall(jobs)

    '''
    missing = check_files(directory, npages)
    print
    print missing
    while (missing != []):
        for m in missing:
            get_files(m, directory)
        missing = check_files(directory)

    get_files(103, directory)
    '''
    return npages

if __name__=='__main__':
    getlist()
