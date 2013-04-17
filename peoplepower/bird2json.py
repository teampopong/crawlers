# coding: utf-8

import json
import collections
import itertools
from pprint import pprint

with open('items.json') as f:
    items = json.load(f)

class info: pass
index = collections.defaultdict(info)
for item in items:
    type = item['type']
    id = item['id']
    info = index[id]
    if type == 'member':
        info.name = item['name']
    elif type == 'special':
        info.party = item['party']

def count_party_change(info):
    return len(info.party)

result = sorted(index.itervalues(), key=count_party_change, reverse=True)
top = itertools.islice(result, 0, 100000)

def party_info(d, row):
    pa = ['party', 'startdate', 'enddate']
    pd = [row[u'정당'], row[u'입당'], row[u'탈당(변경)']]
    pi = dict(zip(pa,pd))
    return pi

with open('output.json', 'w') as f:
    d = dict()
    for info in top:
        n = info.name.split(' ')
        print n
        data = [party_info(d, row) for row in info.party]
        d[n[0]] = data
        pprint(d)
    json.dump(d, f, indent=2)
