#!/usr/bin/env python

#precondition: argument is a short string that will describe a business, and an integer x for the top x businesses
#postcondition: returns a string of the top x businesses in the category searched, retrieved from hoover.com

import sys
import re
import urllib
import urllib2
import json
from bs4 import BeautifulSoup
from itertools import izip_longest
from operator import add

def queryHoovers(biztype, limit=10):
  """
  queries Hoovers for companies of given type
  returns top matches, sorted by sales, up to limit
  output is html
  """

  params = {'type': 'company', 'term': biztype, 'formstep': 0, 'sort': 'sales', 'sortDir': 'desc'}
  response = urllib2.urlopen('http://www.hoovers.com/search/company-search-results/100003765-1-1NJHZ8.html?%s' % urllib.urlencode(params))

  for line in response:
    if re.search('<h1>Company Results</h1>', line):
      filtered = '<html><body>' + line + response.read()
      break

  return filtered


def getCompanies(biztype, limit=10):
  """
  queries Hoovers for companies of given type
  returns top matches, sorted by sales, up to limit
  output is json
  """

  html = queryHoovers(biztype, limit)
  #with open('body.html') as f:
  #  html = f.read()

  soup = BeautifulSoup(html)
  #print("made the soup")
  interleave = lambda a,b: list(filter(None, reduce(add, izip_longest(a,b))))
  rows = interleave(soup.find_all('tr', 're-grey', limit=(limit+1)/2), soup.find_all('tr', 'sr-white', limit=limit/2))

  

  companies = [{'Name':row('td', 'company_name')[0].text, 'Location': row('td', 'company-location')[0].text, 'Sales': row('td', 'company-sales')[0].text} for row in rows]

  #print(companies)
  out = str(json.dumps(companies)) # from unicode to ascii
  out = out.replace('\\u00a0', ' ') # replace non-breaking spaces
  return(out)


if __name__ == '__main__':

  if len(sys.argv) < 2:
    print 'usage: %s biztype limit' % __file__
    exit()
    
  businesses = getCompanies(sys.argv[1], int(sys.argv[2]))
  print businesses
