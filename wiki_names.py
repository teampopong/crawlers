#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import html5lib
import lxml
import urllib2

Settings = {
    'USER_AGENT': "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) "
            "Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5",
            'XPATH_MEMBER_NAMES': "//div[@class='mw-content-ltr']/h3/following-sibling::p/a/text()",
    'START': 1,
    'END': 3
}

def get_pagename(num):
    return '대한민국 제%d대 국회의원 목록' % num

def get_wiki_url(pagename):
    return 'http://ko.wikipedia.org/wiki/%s' % urllib2.quote(pagename)

def get_xpath(url, xpath):
    htmlparser = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)

    request = urllib2.Request(url)
    request.add_header("User-Agent", Settings['USER_AGENT'])
    f=urllib2.urlopen(request)

    page = htmlparser.parse(f)
    return page.xpath(xpath)

def get_member_names(url):
    return get_xpath(url, Settings['XPATH_MEMBER_NAMES'])

if __name__ == '__main__':
    for num in xrange(Settings['START'], Settings['END'] + 1):
        print '%d대' % num
        pagename = get_pagename(num)
        url = get_wiki_url(pagename)
        print ' '.join(get_member_names(url))
        print
