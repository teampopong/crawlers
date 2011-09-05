import re
import itertools
import lxml.html

__all__ = ["convert_to_text", "extract", "extract_text", "extract_table", "extract_ids", "extract_texts", "extract_texts", "extract_url"]

def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def convert_to_text(e):
    texts = []
    texts.append(e.text.strip())
    for br in e:
        assert br.tag == 'br'
        texts.append('\n')
        if e.tail: texts.append(e.tail.strip())
    return ''.join(texts)

def extract(hxs, xpath):
    result = hxs.select(xpath).extract()
    if not result: return ''
    return result[0]

def extract_text(hxs, xpath):
    result = hxs.select(xpath).extract()
    if not result: return ''
    return convert_to_text(lxml.html.fromstring(result[0]))

def extract_table(hxs, xpath):
    count = len(hxs.select('%s/tr[1]/td' % xpath))
    cells = hxs.select('%s//td' % xpath).extract()
    rows = grouper(count, (lxml.html.fromstring(cell).text_content().strip() for cell in cells), '')
    keys = rows.next()
    result = []
    for values in rows:
        if not values[0]: continue
        result.append(dict(zip(keys, values)))
    return result

def extract_ids(hxs, key):
    xpath = '//a[contains(@href, "%s=")]/@href' % key
    return hxs.select(xpath).re(r'%s=(\d+)' % key)

def extract_texts(hxs, key):
    xpath = '//a[contains(@href, "%s=")]/text()' % key
    return hxs.select(xpath).extract()

def extract_url(url, key):
    return re.search(r'%s=(\d+)' % key, url).group(1)
