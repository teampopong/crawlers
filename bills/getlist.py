#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re
import sys
import math
import urllib2
import gevent
from gevent import monkey; monkey.patch_all()

import utils
from settings import BASEURL, DIR, PAGE_SIZE

def get_files(baseurl, page, directory, npages):
    try:
        url = baseurl + '&PAGE=%d&PAGE_SIZE=%d' % (page, PAGE_SIZE)
        pn = npages - page + 1
        fn = '%s/%d.html' % (directory, pn)
        utils.get_webpage(url, fn)
        sys.stdout.write('%s\t' % pn)
        sys.stdout.flush()
    except (urllib2.URLError, IOError) as e:
        print '\nFailed to get %s due to %s' % (fn, e.__repr__)

def get_npages(baseurl, directory):
    fn = '%s/tmp.html' % directory
    utils.get_webpage(baseurl, fn)
    page = utils.read_webpage(fn)
    m = re.search(u'총(.+)건', page.xpath('//span[@class="text3"]/text()')[0])
    nbills = int(m.group(1))
    npages = int(math.ceil(nbills/float(PAGE_SIZE)))
    return nbills, npages

def check_files(directory, npages):
    files = os.listdir(directory)
    nums = [int(f.strip('.html')) for f in files if f!='tmp.html']
    return [m for m in range(1, npages+1) if m not in nums]

def getlist(assembly_id):
    print "## Get meta data"
    url = '%sAGE_FROM=%d&AGE_TO=%d' % (BASEURL['list'], assembly_id, assembly_id)
    directory = '%s/%s' % (DIR['list'], assembly_id)
    utils.check_dir(directory)

    #
    nbills, npages = get_npages(url, directory)
    print 'Total %d bills, %d pages to %s' % (nbills, npages, directory)

    #
    print 'Downloading:'
    jobs = [gevent.spawn(get_files, url, page, directory, npages)\
            for page in range(1, npages+1)]
    gevent.joinall(jobs)

    #
    missing = check_files(directory, npages)
    if missing:
        print 'Missing files:'
        print missing
        while (missing != []):
            for m in missing:
                get_files(url, m, directory, npages)
            missing = check_files(directory)

    #get_files(url, 103, directory, npages)
    return npages

if __name__=='__main__':
    assembly_id = 1
    getlist(assembly_id)
