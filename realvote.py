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

def real_vote(info):
    if not info.election: return 100.0
    assert len(info.election) == 1
    turnout = float(info.election[0][u'투표율'][:-2])
    vote = float(info.election[0][u'득표율'][:-2])
    return turnout * vote / 100.0

result = sorted(index.itervalues(), key=real_vote)
top = itertools.islice(result, 0, 10)

for info in top:
    print info.name, '%.2f %%' % real_vote(info), '=',
    print info.election[0][u'득표율'], '*', info.election[0][u'투표율']
