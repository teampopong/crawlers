#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import html5lib
import itertools
import json
import re
import urllib2

USER_AGENT = "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) "\
            "Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5"

schars_re = re.compile('[/\(\)]')
ws_re = re.compile('\s')

class InvalidCrawlerError(Exception):
    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return ' '.join(self.args)

def flatten(rarray):
    return list(itertools.chain.from_iterable(rarray))

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

def parse_cell(node):
    arr = _parse_cell(node)
    if not arr:
        return ''
    elif len(arr) == 1:
        return arr[0]
    else:
        return arr

def _parse_cell(node):
    parts = ([node.text] +
            flatten(_parse_cell(c) for c in node.getchildren()) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    filtered = itertools.ifilter(None, parts)
    stringified = ((''+x).strip() for x in filtered)
    strings = [x for x in stringified if len(x)]
    return strings

def sanitize(txt):
    return schars_re.sub('', txt)

def split(txt):
    splitted = schars_re.split(txt)
    concatenated = [ws_re.sub('', s) for s in splitted]
    return concatenated
