#!/usr/bin/python
#-*- coding: utf-8 -*-

''' National assembly member crawler (r0, 2011-5-22)
    written by Cheol Kang <steel@popong.com>
    - Currently broken because of the site renewal (2013-08-31)
'''

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urlparse import urljoin
import re
import sys
import urllib2

# constants
DEBUG = False 

# settings
DBG_SAMPLE = 'sample.html'
PAGE_ENC = 'euc-kr'

# global dicts
urls = {}
ppl_urls = {}

# SQLAlchemy things
# TODO: enable 'update' - if a DB already exists, then this code causes error
Base = declarative_base()
Session = sessionmaker()

class Member(Base):
    __tablename__ = 'members'

    name_kr = Column(String, primary_key=True, nullable=False) # 한글이름
    name_cn = Column(String) # 한문이름
    name_en = Column(String) # 영문이름
    birth = Column(String) # 생년월일
    party = Column(String) # 정당
    district = Column(String) # 선거구
    committee = Column(String) # 소속위원회
    when_elected = Column(String) # 당선 횟수
    profile = Column(String) # 약력
    addr = Column(String) # 자택주소
    off_phone = Column(String) # 사무실전화
    aides = Column(String) # 보좌관
    pr_secrs = Column(String) # 비서관
    sc_secrs = Column(String) # 비서
    hobby = Column(String) # 취미/특기
    email = Column(String) # 이메일
    homepage = Column(String) # 홈페이지

    def __init__(self, name_kr, name_cn, name_en, party, district, committee, when_elected, profile, addr, off_phone, aides, pr_secrs, sc_secrs, hobby, email, homepage):
        # TODO: valid check
        self.name_kr = name_kr
        self.name_cn = name_cn
        self.name_en = name_en
        self.party = party
        self.district = district
        self.committee = committee
        self.when_elected = when_elected
        self.profile = profile
        self.addr = addr
        self.off_phone = off_phone
        self.aides = aides
        self.pr_secrs = pr_secrs
        self.sc_secrs = sc_secrs
        self.hobby = hobby
        self.email = email
        self.homepage = homepage

    def __repr__(self):
        return "<Member('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.name_kr, self.name_cn, self.name_en, self.party, self.district, self.committee, self.when_elected, self.profile, self.addr, self.off_phone, self.aides, self.pr_secrs, self.sc_secrs, self.hobby, self.email, self.homepage)

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

def init_db():
    engine = create_engine('sqlite:///members.db', echo='True')
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

def get_page(url):
    page_in_txt = urllib2.urlopen(url).read()
    return page_in_txt

def get_ppl_urls():
    def unescape_html(doc):
        escape_table = {'&lt;': '<', '&gt;': '>', '&amp;': '&'}
        for old, new in escape_table.items():
            doc = doc.replace(old, new)
        return doc

    url_key = 'people_list'
    list_class = 'member-namesearch-resultlist'

    page = get_page(urls[url_key])

    full_member_list = []
    member_lists = getlist_bracketed_regexp(r'<ul class="%s">(.+?)</ul>' % list_class, page)
    for member_list in member_lists:
        full_member_list += getlist_bracketed_regexp(r'<li><a href="(.+?)".*?>(.+?)</a></li>', member_list)

    for url, name in full_member_list:
        url = unescape_html(url)
        ppl_urls[name] = urljoin(urls['base'], url)

def extract_profile(page):
    def parse_name_and_birth(name_and_birth):
        # name_and_birth: e.g. <strong>고승덕 (高承德)</strong><br>Seungduk Koh<br>(1957/11/12)
        tokens = find_bracketed_texts_regexp(r'<strong>(.+?)\s*\((.*?)\)</strong><br\s*/?>(.*?)<br\s*/?>\((.*?)\)', name_and_birth)
        name_kr, name_cn, name_en, birth = tokens
        return (name_kr, name_cn, name_en, birth)

    # get name & birth
    name_and_birth = find_bracketed_text_regexp(r'<div class="name".*?>(.+?)</div>', page)
    name_and_birth = parse_name_and_birth(name_and_birth)

    # get other info
    prof_data = find_bracketed_text_regexp(r'<table class="datatable".*?>(.+?)</table>', page)
    prof_data = tuple(getlist_bracketed_regexp(r'<td>(.*?)</td>', prof_data))

    full_profile = name_and_birth + prof_data
    full_profile = (find_bracketed_text_regexp(r'<a.*?>(.*?)</a>', x) if x.startswith('<a') else x for x in full_profile)
    full_profile = (x.decode(PAGE_ENC) for x in full_profile)
    return full_profile

def crawl_ppl_data():
    session = Session()

    for name, url in ppl_urls.items():
        print name.decode('euc-kr')
        page = get_page(url)
        profile = extract_profile(page)
        member = Member(*profile)
        session.add(member)

    session.commit()
    session.close()

def main(argv):
    if DEBUG:
        page = open(DBG_SAMPLE, 'r').read()
        profile = extract_profile(page)
        for item in profile:
            print item
    else:
        load_urls()
        init_db()
        get_ppl_urls()
        crawl_ppl_data()

if __name__ == '__main__':
    main(sys.argv[1:])
