#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2

def crawl(baseurl, directory, rng=(1,126)):

    for n in range(rng[0], rng[1]+1):
        outp = '%s/%d.html' % (directory, n)

        url = baseurl + str(n)
        r = urllib2.urlopen(url)
        with open(outp, 'w') as f:
            f.write(r.read())
        print '%s to %s' % (n, outp)
