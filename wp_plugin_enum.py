try:
	import requests
	import sys
	import ssl
except Exception,e:
	print "[!] Error: "+str(e)
	print "[*] Make sure you have the following Python modules installed:\n\trequests, sys, ssl"
	exit(0)
if len(sys.argv)!=3:
	print "Usage: %s <path_to_plugins.txt> <target>"%sys.argv[0]
	exit(0)

if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

print "[*] Started"

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

f = open(sys.argv[1],"r")
data = f.readlines()
print "\nNote: Append readme.txt or changelog.txt in same or different letter cases to open version file\n"
for i in data:
	try:
		i = (i.replace("\r","")).replace("\n","")
		r = requests.get(sys.argv[2]+"/wp-content/plugins/"+i+"/", verify=False)
		sc = r.status_code
		if sc != 404 and sc != 500:
			print i + " : " + str(sc) + " : " + sys.argv[2] + "/wp-content/plugins/" + i + "/"
	except:
		print "Exception occurred"
print "[*] Completed"
