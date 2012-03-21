import json
with open('cand-0411.json', 'r') as inp, open('output', 'w') as outp:
    data = json.load(inp, encoding="UTF-8")
    outp.write(\
        '\n'.join(\
            ','.join(\
                map(lambda x: '"'+x.encode('utf8')+'"', datum.values())\
                ) for datum in data))
