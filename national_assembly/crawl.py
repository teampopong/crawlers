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
from scrapy.selector import Selector # pip install Scrapy

# settings
PAGE_ENC = 'utf-8'
HEADERS = ['name_kr','name_cn','name_en','birth','party','district','committee','when_elected','off_phone','homepage','email','aides','pr_secrs','sc_secrs','hobby','experience','photo','url']
DATADIR = '.'

# global dicts
urls = {}
ppl_urls = []
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
def get_xpath_data(data, _xpath):
    xpath_selector_list = []

    hxs = Selector(text=data)
    for i in hxs.xpath(_xpath):
        xpath_selector_list.append(i.extract().encode("utf-8"))
    if len(xpath_selector_list) >0 :
        return  xpath_selector_list[0].decode(PAGE_ENC)
    else:
        return xpath_selector_list.decode(PAGE_ENC)

def get_ppl_urls(htmldir):
    def unescape_html(doc):
        escape_table = {'&lt;': '<', '&gt;': '>', '&amp;': '&'}
        for old, new in escape_table.items():
            doc = doc.replace(old, new)
        return doc

    url_key = 'people_list'
    list_class = 'memberna_list'


    page = get_page(urls[url_key], htmldir)

    full_member_list = []
    member_lists = getlist_bracketed_regexp(r'<dd class="img">(.+?)</dd>', page)
    print len(member_lists)

    #        <dd class="img">
    #            <a href="#" onclick="jsMemPop(2680)" title="강기윤의원정보 새창에서 열림">
    #                   <img src="/photo/9770703.jpg" alt="강기윤 의원사진" />
    #            </a>
    #        </dd>

    for member_list in member_lists:
        full_member_list += getlist_bracketed_regexp(r'<a href="#" onclick="jsMemPop\((.+?)\)".*?>[\r\n\s]*?<img src=".+?" alt="(.+?)".*?/>', member_list)

    for url, name in full_member_list:
        url = unescape_html(url)
        ppl_urls.append(urls['person']+ url)

def extract_profile(page):
    def parse_name_and_birth(name_and_birth):
        #<h4>강기윤</h4>
        #    <ul>
        #      <li class="photo">
        #           <img src="/photo/9770703.jpg" alt="강기윤 의원사진" />
        #      </li>
        #      <li>姜起潤</li>
        #      <li>KANG Gi Yun</li>
        #      <li>1960-06-04</li>
        #   </ul>
        profile = get_xpath_data(page,".//*/div[@class='profile']")
        name_kr = get_xpath_data(profile, ".//*/h4/text()")
        name_cn = Selector(text=profile).xpath('.//*/li/text()')[2].extract()
        name_en = Selector(text=profile).xpath('.//*/li/text()')[3].extract()
        birth = Selector(text=profile).xpath('.//*/li/text()')[4].extract()
        return [name_kr, name_cn, name_en, birth.replace('.','-')]

    # get name & birth
    name_and_birth = parse_name_and_birth(page)

    # get experience
    experience = find_bracketed_texts_regexp(r'<dl class="per_history">.*?<dd.*?>(.+?)</dd>.*?</dl>', page)
    experience = ''.join(experience)
    experience = [d.strip() for d in experience.split('<br />')]
    experience = '||'.join(experience)

    # get photo
    photo = find_bracketed_text_regexp(r'<li class="photo".*?>[\r\n\s]*?<img src="(.+?)".*?/>[\r\n\s]*?</li>', page)
    photo = urljoin(urls['base'], photo)

    # get others
    others = find_bracketed_text_regexp(r'<dl.*?class="pro_detail">(.+?)</dl>', page)
    others = getlist_bracketed_regexp(r'<dd>[\r\t\n\s]*?(.+?)[\r\t\n\s]*?</dd>', others)
    #TODO: I don't know the meaning behind
    try:
        others[5] = re.search(r'<a.*?>(.+?)</a>', others[5]).group(1)
    except AttributeError as e:
        others[5] = ''

    stripped = [re.sub('[\s\r]+', '', i) for i in others]
    full_profile = list(name_and_birth + stripped)
    full_profile.append(experience)
    full_profile.append(photo)
    return [p.replace('"',"'") for p in full_profile]

def crawl_ppl_data(htmldir):
    print len(ppl_urls)
    for i, url in enumerate(ppl_urls):
        page = get_page(url, htmldir)
        profile = extract_profile(page)
        ppl_data.append(profile + [url])
        print i, ppl_data[i][0]

def sort_ppl_data(ppl_data):
    ppl_data = sorted(ppl_data, key=lambda x: x[3])
    ppl_data = sorted(ppl_data, key=lambda x: x[0])

def write_csv():
    with open('assembly.csv', 'w') as f:
        f.write('%s\n' % ','.join(HEADERS))
        f.write('\n'.join(\
            '"%s"' % '","'.join(row) for row in ppl_data).encode('utf-8'))
    print 'Data succesfully written'

def main(argv, datadir=DATADIR):

    htmldir = '%s/html' % datadir
    if not os.path.exists(htmldir):
        os.makedirs(htmldir)

    load_urls()
    get_ppl_urls(htmldir)
    crawl_ppl_data(htmldir)
    sort_ppl_data(ppl_data)
    write_csv()

if __name__ == '__main__':
    main(sys.argv[1:])
