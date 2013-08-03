#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib2

def crawl(baseurl, directory, rng=(1,4)):

    for n in range(rng[0], rng[1]+1):
        outp = '%s/%d.html' % (directory, n)
        if n==1:
            m = ''
        else:
            m = str(n)

        url = '%s%s.htm' % (baseurl, m)
        r = urllib2.urlopen(url)
        with open(outp, 'w') as f:
            f.write(r.read())
        print '%s to %s' % (n, outp)
