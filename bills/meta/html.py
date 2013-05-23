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
    baseurl = '%sAGE_FROM=%d&AGE_TO=%d' % (BASEURL['list'], assembly_id, assembly_id)
    directory = '%s/%s' % (DIR['list'], assembly_id)
    return baseurl, directory

def get_npages(assembly_id):
    url, directory = convert(assembly_id)
    utils.check_dir(directory)

    fn = '%s/tmp.html' % directory
    utils.get_webpage(url, fn)
    page = utils.read_webpage(fn)
    m = re.search(u'총(.+)건', page.xpath('//span[@class="text3"]/text()')[0])
    nbills = int(m.group(1))
    npages = int(math.ceil(nbills/float(PAGE_SIZE)))
    print 'Total %d bills, %d pages to %s' % (nbills, npages, directory)
    return npages

def get_html(assembly_id, npages):

    def get_page(baseurl, page, directory, npages):
        try:
            url = baseurl + '&PAGE=%d&PAGE_SIZE=%d' % (page, PAGE_SIZE)
            pn = npages - page + 1
            fn = '%s/%d.html' % (directory, pn)

            is_first = True
            while is_first or 'TEXTAREA ID="MSG" STYLE="display:none"' in doc:
                r = urllib2.urlopen(url)
                doc = r.read()
                is_first = False

            with open(fn, 'w') as f:
                f.write(doc)

            sys.stdout.write('%s\t' % pn)
            sys.stdout.flush()

        except (urllib2.URLError, IOError) as e:
            print '\nFailed to get %s due to %s' % (fn, e.__repr__)

    baseurl, directory = convert(assembly_id)
    utils.check_dir(directory)

    #
    print 'Downloading:'
    jobs = [gevent.spawn(get_page, baseurl, page, directory, npages)\
            for page in range(1, npages+1)]
    gevent.joinall(jobs)

    return npages
