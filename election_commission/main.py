#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

from argparse import ArgumentParser
import codecs
import gevent
from gevent import monkey
import json
from types import UnicodeType

from crawlers import Crawler
from crawlers.local.static import get_election_type_name
from utils import check_dir

def print_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, encoding="UTF-8", indent=2)

def print_csv(filename, data):

    def transform(txt):
        if isinstance(txt, int):
            txt = str(txt)
        if isinstance(txt, list):
            txt = '||'.join(txt)
        txt = txt.replace(',', '|')
        if isinstance(txt, UnicodeType):
            txt = txt.encode('utf8')
        return txt

    attrs = ['assembly_no', 'district', 'cand_no', 'party', 'name_kr',
             'name_cn', 'sex', 'birthyear', 'birthmonth', 'birthday',
             'address', 'job', 'education', 'experience', 'recommend_priority',
             'votenum', 'voterate', 'elected']

    with open(filename, 'w') as f:
        f.write(codecs.BOM_UTF8)
        f.write(','.join(attrs))
        f.write('\n')
        for cand in data:
            values = (cand[attr] if attr in cand else '' for attr in attrs)
            values = (transform(value) for value in values)
            f.write(','.join(values))
            f.write('\n')

def crawl(target, _type, nth, printer, filename, level):
    crawler = Crawler(target, _type, nth, level)
    cand_list = crawler.crawl()
    printer(filename, cand_list)

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('target', choices=['assembly', 'local', 'president'],\
            help="name of target election")
    parser.add_argument('type', choices=['candidates', 'elected', 'precandidates'],
            help="type of person")
    parser.add_argument('start', help="starting election id", type=float)
    parser.add_argument('end', help="ending election id", type=float,\
            nargs='?', default=None)
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-d', '--directory', help="specify data directory")

    # TODO: change to subparser
    parser.add_argument('-l', '--level', choices=[
        'pg', 'province_governor',
        'pm', 'province_member',
        'mg', 'municipality_governor',
        'mm', 'municipality_member',
        'eg', 'education_governor',
        'em', 'education_member'],
        help="Specify level for local elections")
    return  parser

def main(args):
    printer = print_csv if args.test else print_json
    filetype = 'csv' if args.test else 'json'
    datadir = args.directory if args.directory else './data'
    check_dir(datadir)

    if args.target=='local':
        if args.end:
            jobs = []
            args.level = get_election_type_name(args.level)
            for n in xrange(args.start, args.end+1):
                filename = '%s/%s-%s-%s-%d.%s'\
                    % (datadir, args.target, args.level, args.type, n, filetype)
                job = gevent.spawn(crawl, target=args.target, level=args.level,\
                    _type=args.type, nth=n, filename=filename, printer=printer)
                jobs.append(job)
            gevent.joinall(jobs)
        else:
            n = args.start
            args.level = get_election_type_name(args.level)
            filename = '%s/%s-%s-%s-%.01f.%s' %\
                    (datadir, args.target, args.level, args.type, n, filetype)
            crawl(target=args.target, level=args.level, _type=args.type, nth=n,\
                        filename=filename, printer=printer)
    else:
        if args.end:
            jobs = []
            for n in xrange(args.start, args.end+1):
                filename = '%s/%s-%s-%d.%s'\
                        % (datadir, args.target, args.type, n, filetype)
                job = gevent.spawn(crawl, target=args.target, _type=args.type, nth=n,\
                        filename=filename, printer=printer)
                jobs.append(job)
            gevent.joinall(jobs)
        else:
            n = args.start
            filename = '%s/%s-%s-%.01f.%s' %\
                    (datadir, args.target, args.type, n, filetype)
            crawl(target=args.target, _type=args.type, nth=n,\
                        filename=filename, printer=printer)
    print 'Data written to %s' % filename

if __name__ == '__main__':
    monkey.patch_all()
    parser = create_parser()
    args = parser.parse_args()
    main(args)
