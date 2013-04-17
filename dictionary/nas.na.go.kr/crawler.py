#! /usr/bin/python2.7
# -*- coding: utf-8 -*-


from spynner import Browser
from pyquery import PyQuery

browser = Browser()
browser.set_html_parser(PyQuery)

browser.load("http://en.wikipedia.org/wiki/List_of_U.S._states")

# get the table of states
table = browser.soup("table.wikitable")
# skip the first row, which contains only column names
rows = table("tr")[1:]

pop_dict = {}
for row in rows:
    columns = row.findall("td")
    state_name = columns[0].find('a').text
    population = int(columns[6].text.replace(',', ''))
    pop_dict[state_name] = population

print pop_dict

