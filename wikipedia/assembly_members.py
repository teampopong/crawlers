#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import re
import html5lib
import urllib2

settings  = {
        "HEADERS": ["assembly_id", "name", "url"],
        "USER_AGENT": "Mozilla/5.0",
        "X_PATH": "//div[@id='bodyContent']//p/a"
        }

def get_xpaths(assembly_id):
    url = "http://ko.wikipedia.org/wiki/대한민국_제%s대_국회의원_목록"\
            % assembly_id
    p = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)
    r = urllib2.Request(url)
    r.add_header("User-Agent", settings["USER_AGENT"])
    f = urllib2.urlopen(r)

    page = p.parse(f)
    xpaths = page.xpath(settings["X_PATH"])
    return xpaths

def parse_data(assembly_id, xpaths):

    def is_valid(name):
        if len(name) < 2 or re.match(ur'[0-9]+월 [0-9]+일|[0-9]+년', name):
            return False
        return True

    data = []
    for x in xpaths:
        name = x.xpath("text()")[0]
        path = x.xpath("@href")[0]
        if is_valid(name):
            data.append(",".join([str(assembly_id), name.encode("utf-8"), path]))
    return data

def write_csv(filename, headers, data):
    with open(filename, "w") as f:
        f.write(",".join(headers) + "\n")
        f.write("\n".join(data))

if __name__ == "__main__":
    data = []
    for assembly_id in range(2, 19+1):
        data.extend(parse_data(assembly_id, get_xpaths(assembly_id)))
    write_csv("assembly_members.csv", settings["HEADERS"], data)
