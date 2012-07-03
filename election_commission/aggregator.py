# -*- encoding: utf-8 -*-

class PeopleAggregator(object):

    data = {}

    def __init__(self, *keys):
        self.keys = keys

    def _key(self, person):
        return tuple(person.get(key, None) for key in self.keys)

    def insert(self, person):
        if isinstance(person, list):
            for p in person:
                self.insert(p)
            return

        key = self._key(person)
        entry = self.data.get(key, None)

        if not entry:
            entry = {}
            self.data[key] = entry

        for attr, val in person.items():
            if val in ['', None]: continue

            if attr not in entry:
                entry[attr] = set()
            entry[attr].add(val)

    def get_all(self):
        for idx, (key, person) in enumerate(self.data.items()):

            # convert from set to list
            for attr, val in person.items():
                val = list(val) if len(val) > 1 else val.pop()
                person[attr] = val

            # numbering
            person['id'] = idx

        return list(self.data.values())

def main(argv):
    if not argv:
        print('[ERROR] filename not specified')
        print('Usage: aggregator.py [<file>]+')
        print('  file: json file that contains a list of people data')
        return 1

    aggregator = PeopleAggregator('name_kr', 'birthyear', 'birthmonth', 'birthday')

    import json
    for filename in argv:
        print('aggregating %s' % (filename))
        with open(filename, 'r') as f:
            people = json.load(f, encoding='UTF-8')
            aggregator.insert(people)

    people = aggregator.get_all()
    with open('aggregated.json', 'w') as f:
        json.dump(people, f, indent=2)

if __name__ == '__main__':
    import sys
    code = main(sys.argv[1:] or 0)
    sys.exit(code)
