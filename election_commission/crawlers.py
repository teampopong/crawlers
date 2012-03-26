#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from urlparse import urljoin
import re

from utils import get_json, get_xpath, stringify

class Crawler19:
    url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json?electionId=0020120411&electionCode=2'
    url_cand_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml?electionId=0020120411&requestURI=%2Felectioninfo%2F0020120411%2Fcp%2Fcpri03.jsp&statementId=CPRI03_%232&electionCode=2&sggCityCode=0&cityCode='
    url_image_base = 'http://info.nec.go.kr'

    attrs = ['district', 'image', 'cand_no', 'party', 'name', 'sex',
            'birth', 'address', 'job', 'education', 'experience']

    regex_split = re.compile('[/\(\)\s]')

    def city_codes(self):
        list_ = get_json(self.url_city_codes_json)['body']
        return map(lambda x: x['CODE'], list_)

    def url_cand_list(self, city_code):
        return self.url_cand_list_base + str(city_code)

    def parse_member(self, member):
        for attr in self.attrs:
            if attr not in ['name', 'image']:
                member[attr] = stringify(member[attr]).strip()

        # never change the order
        self.parse_member_image(member)
        self.parse_member_pledge(member)
        self.parse_member_name(member)
        self.parse_member_birth(member)
        self.parse_member_experience(member)

        return member

    def parse_member_image(self, member):
        rel_path = member['image'].find("./input[@type='image']").attrib['src']
        member['image'] = urljoin(self.url_image_base, rel_path)

    def parse_member_name(self, member):
        txt = stringify(member['name']).strip()
        member['name_kr'], member['name_cn'] = re.split(self.regex_split, txt)[:2]
        member['name'] = member['name_kr']

    def parse_member_pledge(self, member):
        pass # TODO: implement

    def parse_member_birth(self, member):
        member['birthyear'], member['birthmonth'], member['birthday'] =\
                re.split(self.regex_split, member['birth'])[:3]
        del member['birth']

    def parse_member_experience(self, member):
        pass # TODO: 이거 구현하면 parse_member도 고쳐야 함

    def parse_cand_page(self, url):
        elems = get_xpath(url, '//td')
        members = (dict(zip(self.attrs, elems[i*11:(i+1)*11]))\
                    for i in xrange(len(elems) / 11))

        members = [self.parse_member(member) for member in members]
        return members

    def crawl(self):
        cand_list = []
        for city_code in self.city_codes():
            req_url = self.url_cand_list(city_code)
            dist_cand_list = self.parse_cand_page(req_url)
            cand_list.extend(dist_cand_list)
            print 'crawled %d candidates...' % (len(cand_list),)
            break

        return cand_list
