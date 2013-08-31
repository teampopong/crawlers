#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
Korean National Assembly member crawler
- 2011-05-22 Written by Cheol Kang <steel@popong.com>
- 2013-08-31 Rewritten by Lucy Park <lucypark@popong.com>
"""

from urlparse import urljoin
import os
import re
import sys
import urllib2

# settings
PAGE_ENC = 'euc-kr'
HEADERS = ['name_kr','name_cn','name_en','birth','party','district','committee','when_elected','off_phone','homepage','email','aides','pr_secrs','sc_secrs','hobby','experience','photo','url']
DATADIR = '.'

# global dicts
urls = {}
ppl_urls = {}
ppl_data = []

def find_bracketed_text_regexp(exp, src):
    return re.search(exp, src, flags=re.DOTALL).group(1)

def find_bracketed_texts_regexp(exp, src):
    return re.search(exp, src, flags=re.DOTALL).groups(1)

def getlist_bracketed_regexp(exp, src):
    return re.findall(exp, src, flags=re.DOTALL)

def load_urls():
    for line in open('urls', 'r'):
        if line[0] == '#':
            continue
        key, url = line.split()
        urls[key] = url

def get_page(url, htmldir):
    page_in_txt = urllib2.urlopen(url).read()

    idx = url.find('memCode=')
    if idx != -1:
        filename = '%s/%s.html' % (htmldir, url[idx + len('memCode='):])
    else:
        filename = '%s/index.html' % htmldir

    with open(filename, 'w') as f:
        f.write(page_in_txt)
    return page_in_txt.decode(PAGE_ENC)

def get_ppl_urls(htmldir):
    def unescape_html(doc):
        escape_table = {'&lt;': '<', '&gt;': '>', '&amp;': '&'}
        for old, new in escape_table.items():
            doc = doc.replace(old, new)
        return doc

    url_key = 'people_list'
    list_class = 'wii_list'

    page = get_page(urls[url_key], htmldir)

    full_member_list = []
    member_lists = getlist_bracketed_regexp(r'<ul class="%s">(.+?)</ul>' % list_class, page)
    for member_list in member_lists:
        full_member_list += getlist_bracketed_regexp(r'<li class=".*?">[\r\n\s]*?<div class="fl"><a href="(.+?)".*?><img src=".+?" alt="(.+?)".*?>.*?</li>', member_list)

    for url, name in full_member_list:
        url = unescape_html(url)
        ppl_urls[name] = urljoin(urls['base'], url)

def extract_profile(page):
    def parse_name_and_birth(name_and_birth):
        # name_and_birth example:
        #        <strong>김윤덕</strong> (金潤德)<br>
        #        <strong class="txt_s">KIM Yunduk</strong><br>
        #        <span class="txt_e txt_s">1966.05.23</span>
        tokens = find_bracketed_texts_regexp(r'<strong>(.+?)</strong>\s\((.+?)\)<br\s*/?>.*?<strong class="txt_s">(.*?)</strong><br\s*/?>.*?<span class="txt_e txt_s">(.*)</span>', name_and_birth)
        name_kr, name_cn, name_en, birth = tokens
        return [name_kr, name_cn, name_en, birth.replace('.','-')]

    # get name & birth
    name_and_birth = find_bracketed_text_regexp(r'<div class="fl l10 vb t70".*?>(.+?)</div>', page)
    name_and_birth = parse_name_and_birth(name_and_birth)

    # get experience
    experience = find_bracketed_text_regexp(r'<ul class="history l05".*?>.*?<li.*?>(.+?)</li>.*?</ul>', page)
    experience = [d.strip() for d in experience.split('<br>')]
    experience = '||'.join(experience)

    # get photo
    photo = find_bracketed_text_regexp(r'<div class="fl img_box".*?><img src="(.+?)".*?>.*?</div>', page)
    photo = urljoin(urls['base'], photo)

    # get others
    others = find_bracketed_text_regexp(r'<table.*?class="view_type03".*?>.*?<tbody>(.+?)</tbody>.*?</table>', page)
    others = getlist_bracketed_regexp(r'<td.*?>(.*?)</td>', others)
    try:
        others[5] = re.search(r'<a.*?>(.+?)</a>', others[5]).group(1)
    except AttributeError as e:
        pass

    full_profile = list(name_and_birth + others)
    full_profile.append(experience)
    full_profile.append(photo)
    return full_profile

def crawl_ppl_data(htmldir):
    print len(ppl_urls)
    for i, (name, url) in enumerate(ppl_urls.items()):
        print i, name
        page = get_page(url, htmldir)
        profile = extract_profile(page)
        ppl_data.append(profile + [url])

def write_csv():
    with open('data.csv', 'w') as f:
        f.write('%s\n' % ','.join(HEADERS))
        f.write('\n'.join(\
            '"%s"' % '","'.join(row) for row in ppl_data).encode('utf-8'))

def main(argv, datadir=DATADIR):

    htmldir = '%s/html' % datadir
    if not os.path.exists(htmldir):
        os.makedirs(htmldir)

    load_urls()
    get_ppl_urls(htmldir)
    crawl_ppl_data(htmldir)
    write_csv()

if __name__ == '__main__':
    main(sys.argv[1:])
