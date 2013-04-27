#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2

directory = 'html/'
base = 'http://nas.na.go.kr/site?siteId=site-20111206-000001000&pageId=page-20111207-000001129&dic_mode=default&dic_pageNumber='
num = 126
ext = '.html'

if not os.path.exists(directory):
    os.makedirs(directory)

for n in range(1, num+1):

    outp = directory + str(n) + ext

    url = base + str(n)
    r = urllib2.urlopen(url)
    with open(outp, 'w') as f:
        f.write(r.read())
    print '%s to %s' % (n, outp)
