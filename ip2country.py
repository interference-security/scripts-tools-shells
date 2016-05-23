#!/usr/bin/python
import requests
import sys

if len(sys.argv)<=1:
	print "Usage: "+sys.argv[0]+" <ip-list.txt>"

f = open(sys.argv[1],"r")
data = f.readlines()
for ip in data:
	ip = (ip.replace("\r","")).replace("\n","")
	try:
		temp = requests.get("http://ip-api.com/csv/"+ip,timeout=120)
		resp = temp.content
		d = resp.split(",")
		print ip+","+d[1]
	except:
		print ip+","+"Failed"
