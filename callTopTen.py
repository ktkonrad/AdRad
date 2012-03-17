#!/usr/local/bin/python
import sys
import subprocess
from getTopTen import getTopTen

def printer(search, number):
	x=getTopTen(search, number)	
	print(x)
printer(sys.argv[1],sys.argv[2])
