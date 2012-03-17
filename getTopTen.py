#!/usr/local/bin/python

#precondition: argument is a short string that will describe a business, and an integer x for the top x businesses
#postcondition: returns a string of the top x businesses in the category searched, retrieved from hoover.com

import sys
import re
import urllib2
from bs4 import BeautifulSoup


def getTopTen (biztype="guns", x=10):
	print("getTopTen started with arguments " + biztype+" " +str(x))
	x=int(x)
	biztype = re.sub("\s+","%20",biztype)

	f = urllib2.urlopen('http://www.hoovers.com/search/company-search-results/100003765-1-1NJHZ8.html?type=company&term=' + biztype + '&formstep=0&sort=sales&sortDir=desc')
	#print("opened the url\n")
	s=f.read()

	soup = BeautifulSoup(s)
	#print("made the soup")
	companies = soup("td", {"class" : "company_name"},limit=x)

	#iterates through the specified number of top businesses
	for i in range(x):
		#print("in the loop. i = " + str(i) +"\n")			
		companies[i]=companies[i].next_element.text    #next line after class match is where the actual company name is
		companies[i]=re.sub("\(.*\)","",companies[i])  #gets rid of some parenthetical extras
	
	#print(companies)
	return(companies)

getTopTen(sys.argv[1],int(sys.argv[2]))
