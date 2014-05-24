import os


def tostr(sel):
    return ''.join(l.strip() for l in sel.extract())


def save_file(path, content):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(path, 'w') as f:
        f.write(content)

