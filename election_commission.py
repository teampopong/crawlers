#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import html5lib
from lxml import etree
import urllib2
from urlparse import urljoin
import json
import re

Settings = {
    'USER_AGENT': "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) "
            "Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5",
    'START': 19,
    'END': 19
}

url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json?electionId=0020120411&electionCode=2'
url_cand_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml?electionId=0020120411&requestURI=%2Felectioninfo%2F0020120411%2Fcp%2Fcpri03.jsp&statementId=CPRI03_%232&electionCode=2&sggCityCode=0&cityCode='
url_image_base = 'http://info.nec.go.kr'

attrs = ['district', 'image', 'cand_no', 'party', 'name', 'sex',
        'birth', 'address', 'job', 'education', 'experience']

regex_split = re.compile('[/\(\)\s]')

def get_json(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent", Settings['USER_AGENT'])
    f = urllib2.urlopen(request)
    txt = f.read()
    return json.loads(txt, encoding='UTF-8')

def get_xpath(url, xpath):
    htmlparser = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)

    request = urllib2.Request(url)
    request.add_header("User-Agent", Settings['USER_AGENT'])
    f=urllib2.urlopen(request)

    page = htmlparser.parse(f)
    return page.xpath(xpath)

def city_codes():
    list_ = get_json(url_city_codes_json)['body']
    return map(lambda x: x['CODE'], list_)

def url_cand_list(city_code):
    return url_cand_list_base + str(city_code)

def stringify(node):
    parts = ([node.text] +
            [stringify(c) for c in node.getchildren()] +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def parse_member(member):
    for attr in attrs:
        if attr not in ['name', 'image']:
            member[attr] = stringify(member[attr]).strip()

    # never change the order
    parse_member_image(member)
    parse_member_pledge(member)
    parse_member_name(member)
    parse_member_birth(member)
    parse_member_experience(member)

    return member

def parse_member_image(member):
    rel_path = member['image'].find("./input[@type='image']").attrib['src']
    member['image'] = urljoin(url_image_base, rel_path)

def parse_member_name(member):
    txt = stringify(member['name']).strip()
    member['name_kr'], member['name_cn'] = re.split(regex_split, txt)[:2]
    member['name'] = member['name_kr']

def parse_member_pledge(member):
    pass # TODO: implement

def parse_member_birth(member):
    member['birthyear'], member['birthmonth'], member['birthday'] =\
            re.split(regex_split, member['birth'])[:3]
    del member['birth']

def parse_member_experience(member):
    pass # TODO: 이거 구현하면 parse_member도 고쳐야 함

def parse_cand_page(url):
    elems = get_xpath(url, '//td')
    members = (dict(zip(attrs, elems[i*11:(i+1)*11]))\
                for i in xrange(len(elems) / 11))

    members = [parse_member(member) for member in members]
    return members

def crawl19():
    cand_list = []
    for city_code in city_codes():
        req_url = url_cand_list(city_code)
        dist_cand_list = parse_cand_page(req_url)
        cand_list.extend(dist_cand_list)
        print 'crawling %d candidates...' % (len(cand_list),)

    return cand_list

def crawl(target, output):
    if 1 <= target <= 16:
        pass # TODO: not implemented yet
    elif 17 <= target <= 18:
        pass # TODO: not implemented yet
    elif 19 <= target <= 19:
        cand_list = crawl19()

    with open(output, 'w') as f:
        json.dump(cand_list, f)

def main():
    for n in xrange(Settings['START'], Settings['END']+1):
        filename = 'cand-%d.json' % (n,)
        crawl(target=n, output=filename)

if __name__ == '__main__':
    main()
