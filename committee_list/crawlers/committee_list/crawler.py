#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2

def crawl(url, directory, rng=None):
    r = urllib2.urlopen(url)
    with open('%s/1.html' % directory, 'w') as f:
        f.write(r.read())
    print '1 to %s/1.html' % directory