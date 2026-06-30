#!/usr/bin/env python3

#
# scrape-classes.py: Scrape rule IDs for each 20x class and
# write them to standard output as a CSV file.
#
# Note: requires beautifulsoup4
#
# Example:
#
#   # scrape rule ids by class, save to "class-ids.csv"
#   $ python3 scrape-class-ids.py > class-ids.csv
#

import bs4, csv, re, sys, urllib.request as U

URL = 'https://www.fedramp.gov/20x/'

def query(url: str, css: str) -> list:
  '''fetch URL, parse as HTML, return matching elements'''
  return bs4.BeautifulSoup(U.urlopen(url), features='lxml').css.select(css)

# fetch URLs, match rows
rows = [[c_a.text[-1:], e.text] for c_a in query(URL, 'article.certification-card h3 a[href]') for rs_a in query(c_a['href'], 'table td a[href]') for e in query(U.urljoin(c_a['href'], rs_a['href']), 'summary') if re.match(r'^[A-Z]{3}-[A-Z]{3}-[A-Z]{3}$', e.text)]

# write csv to stdout
csv.writer(sys.stdout).writerows([['class', 'id']] + rows)
