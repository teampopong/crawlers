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
        info.election = item['election']

def vote_turnout(info):
    if not info.election: return 100.0
    assert len(info.election) == 1
    return float(info.election[0][u'투표율'][:-2])

result = sorted(index.itervalues(), key=vote_turnout)
top = itertools.islice(result, 0, 10)

for info in top:
    print info.name, info.election[0][u'투표율']
