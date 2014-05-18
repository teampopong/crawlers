import os


def tostr(sel):
    return ''.join(l.strip() for l in sel.extract())


def save_file(path, content):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path))

    with open(path, 'w') as f:
        f.write(content)

