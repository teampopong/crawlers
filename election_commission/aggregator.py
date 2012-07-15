# -*- encoding: utf-8 -*-

class PeopleAggregator(object):

    data = {}
    fields_key = ['name_kr', 'sex', 'birthyear', 'birthmonth', 'birthday']

    def _key(self, person):
        return tuple(person.get(field, None) for field in self.fields_key)

    def _copy(self, _from, _to, fields=None):
        if not fields:
            fields = _from.keys()

        for field in fields:
            if field in _from and _from[field] not in ['', None]:
                _to[field] = _from[field]

    def insert(self, person):
        if isinstance(person, list):
            for p in person:
                self.insert(p)
            return

        key = self._key(person)
        entry = self.data.get(key, None)

        if not entry:
            entry = {
                    'assembly': {}
                    }
            self.data[key] = entry

        # 국회별 정보 업데이트
        assembly_no = person['assembly_no']
        entry['assembly'][assembly_no] = {}
        self._copy(person, entry['assembly'][assembly_no])

        # 최신 정보 업데이트
        if 'assembly_no' not in entry or entry['assembly_no'] < assembly_no:
            self._copy(person, entry)

    def get_all(self):
        return self.data.values()

def main(argv):
    if not argv:
        print('[ERROR] filename not specified')
        print('Usage: aggregator.py [<file>]+')
        print('  file: json file that contains a list of people data')
        return 1

    aggregator = PeopleAggregator()

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
