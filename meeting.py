# coding: utf-8

import json
import collections
import operator
import itertools

with open('items.json') as f:
    items = json.load(f)

index = collections.defaultdict(int)
for item in items:
    if item['type'] != 'attend': continue
    if item['status'] != u'출석': continue
    index[item['meeting']] += 1

result = sorted(index.iteritems(), key=operator.itemgetter(1))
top = itertools.islice(result, 0, 10)

for meeting, count in top:
    print meeting, '%d명' % count
