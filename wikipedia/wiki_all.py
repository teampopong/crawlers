#!/usr/bin/python
# -*- encoding=utf-8 -*-

import re

class Skip(Exception): pass

pattern_has_district = re.compile(r'(?:\|\|\s*)\[\[(.+?)\]\]\((.+?)\).*?\|\|\s*(.+?)\s*?\|\|')
pattern_no_district = re.compile(r'(?!\|\|\s*)\[\[(.+?)\]\]\((.+?)\).*?\|\|\s*(.+?)\s*?\|\|')

def parse_line(line):
    m = pattern_has_district.search(line)
    if not m: m = pattern_no_district.search(line)

    if not m: # 사람을 나타내는 줄이 아니면 파싱 종료
        raise Skip()

    name_kr, name_cn, party = m.groups()
    name_kr = name_kr.rsplit('|', 1)[-1]\
            .strip(' [')
    parties = party.rsplit('|', 1)[-1]\
                   .split('<br />')
    parties = (party.strip(' []') for party in parties)

    return name_kr, name_cn, parties

for line in open('18th.txt', 'r'):
    try:
        name_kr, name_cn, parties = parse_line(line)
        for party in parties:
            print ','.join((party, name_kr, name_cn))

    except Skip:
        pass
