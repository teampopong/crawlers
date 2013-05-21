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

def convert(assembly_id):
    url = '%sAGE_FROM=%d&AGE_TO=%d' % (BASEURL['list'], assembly_id, assembly_id)
    directory = '%s/%s' % (DIR['list'], assembly_id)
    return url, directory

def get_npages(assembly_id):
    url, directory = convert(assembly_id)

    fn = '%s/tmp.html' % directory
    utils.get_webpage(url, fn)
    page = utils.read_webpage(fn)
    m = re.search(u'총(.+)건', page.xpath('//span[@class="text3"]/text()')[0])
    nbills = int(m.group(1))
    npages = int(math.ceil(nbills/float(PAGE_SIZE)))
    print 'Total %d bills, %d pages to %s' % (nbills, npages, directory)
    return npages

def get_html(assembly_id, npages):
    def get_files(base, page, directory, npages):
        try:
            url = base + '&PAGE=%d&PAGE_SIZE=%d' % (page, PAGE_SIZE)
            pn = npages - page + 1
            fn = '%s/%d.html' % (directory, pn)
            utils.get_webpage(url, fn)
            sys.stdout.write('%s\t' % pn)
            sys.stdout.flush()
        except (urllib2.URLError, IOError) as e:
            print '\nFailed to get %s due to %s' % (fn, e.__repr__)

    def check_files(directory, npages):
        files = os.listdir(directory)
        nums = [int(f.strip('.html')) for f in files if f!='tmp.html']
        return [m for m in range(1, npages+1) if m not in nums]

    url, directory = convert(assembly_id)
    utils.check_dir(directory)

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

    return npages
