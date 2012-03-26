#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import html5lib
import json
import urllib2

USER_AGENT = "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) "\
            "Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5"

class InvalidTargetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '잘못된 대수: %s' % str(value)

def get_json(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    f = urllib2.urlopen(request)
    txt = f.read()
    return json.loads(txt, encoding='UTF-8')

def get_xpath(url, xpath):
    htmlparser = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)

    request = urllib2.Request(url)
    request.add_header("User-Agent", USER_AGENT)
    f=urllib2.urlopen(request)

    page = htmlparser.parse(f)
    return page.xpath(xpath)

def stringify(node):
    parts = ([node.text] +
            [stringify(c) for c in node.getchildren()] +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))
