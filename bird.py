# coding: utf-8

import json
import collections
import itertools

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
top = itertools.islice(result, 0, 5)

for info in top:
    print info.name, len(info.party)
    print ' -> '.join(row[u'정당'] for row in info.party)
    print
