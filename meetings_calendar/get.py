#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import io
import urllib2
import html5lib
import datetime
import re
import sys

base_url = 'http://www.assembly.go.kr/renew10/anc/schedule/assm/assemact/council/council0101/assmSchCal/assemSchCalInfoAjax.do?currentPage=&movePageNum=&rowPerPage=1000&gubun=&agendaid=&committee_id=&board_id=&record_id=&returnPage=&weekday=&today=&calendarMove=&showDt=&meetingday=%s'

link_url = 'http://www.assembly.go.kr/renew10/anc/schedule/assm/assemact/council/council0101/assmSchCal/assemScanCalDetail.do?gubun=%s&agendaid=%s&committee_id=%s&board_id=%s&record_id=%s'

sources_dir = './sources'

header = '"date","time","type","title","session","sitting","committee","url"\n'

xpath_title = '//a[contains(@onclick, "jsDetail")]/text()'
xpath_link_params = '//a[contains(@onclick, "jsDetail")]/@onclick'
xpath_datetime = '//dd/text()'
xpath_committee = '//dd/span/text()'

def is_dashed(str):
	if str.count('-') > 0:
		return True
	else:
		return False

def crawl(url, directory, filename):
	if not os.path.exists(directory):
		os.makedirs(directory)

	r = urllib2.urlopen(url)
	with open('%s/%s.html' % (directory, filename), 'w') as f:
		f.write(r.read())

def get_webpage(f):
	page = html5lib.HTMLParser(\
		tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
		namespaceHTMLElements=False)
	p = page.parse(f, encoding='utf-8')
	return p

def get_link_url(gubun, agendaid, committee_id, board_id, record_id):
	return (link_url % (gubun, agendaid, committee_id, board_id, record_id))

def parse_meeting_schedule(filename):
	date_length = len('0000-00-00') + 1

	session_re = re.compile(u'제(?P<session>[0-9]+)회')
	sitting_re = re.compile(u'제(?P<sitting>[0-9]+)차')

	with open(filename, 'r') as f:
		p = get_webpage(f)

		raw_titles = p.xpath(xpath_title)[0:]
		link_params = p.xpath(xpath_link_params)[0:]
		datetimes = p.xpath(xpath_datetime)[0:]
		committes = p.xpath(xpath_committee)[0:]

		datetimes = [datetime for datetime in datetimes if datetime.strip() != '']
		link_params = [link_param.replace('jsDetail(', '').replace(');return false;', '') for link_param in link_params]

		dates = [datetime[:date_length].strip() for datetime in datetimes]
		times = [datetime[date_length:].strip() for datetime in datetimes]
		types = [title[title.find('[')+1:title.find(']')] for title in raw_titles]
		titles = [title[title.find(']')+2:] for title in raw_titles]
		sessions = [session_re.findall(title)[0] for title in titles]
		sittings = [sitting_re.findall(title)[0] for title in titles]
		links = [eval('get_link_url(%s)' % link_param) for link_param in link_params]

		return zip(dates, times, types, titles, sessions, sittings, committes, links)

def get_meeting_list(start, end):
	if is_dashed(start):
		start = start.replace('-', '')

	if is_dashed(end):
		end = end.replace('-', '')

	startDt = datetime.datetime.strptime(start, '%Y%m%d').date()
	endDt = datetime.datetime.strptime(end, '%Y%m%d').date()

	td = datetime.timedelta(days=1)

	csv_filename = 'meetings_%s_%s.csv' % (start, end)

	with open('%s/%s' % (sources_dir, csv_filename), 'wa') as f:
		f.write(header.encode('utf-8'))
		while startDt <= endDt:
			filename = str(startDt).replace('-', '')
			crawl(('%s' % base_url) % filename, sources_dir, filename)
			result = parse_meeting_schedule(('%s/%s.html' % (sources_dir, filename)))
			f.write('\n'.join(\
				['"%s","%s","%s","%s","%s","%s","%s","%s"' % (date, time, type, title, session, sitting, committee, link) for date, time, type, title, session, sitting, committee, link in result]
				).encode('utf-8'))
			f.write('\n')
			startDt = startDt + td

	print 'parsed to %s' % csv_filename

if __name__=='__main__':
	if len(sys.argv) is 1:
		print 'usage: python get.py YYYY-MM-DD YYYY-MM-DD'
		print '       python get.py YYYY-MM-DD'
	elif len(sys.argv) is 2:
		get_meeting_list(sys.argv[1], sys.argv[1])
	elif len(sys.argv) is 3:
		get_meeting_list(sys.argv[1], sys.argv[2])
