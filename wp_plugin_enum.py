try:
	import requests
	import argparse
	import ssl
except Exception,e:
	print "[!] Error: "+str(e)
	print "[*] Make sure you have the following Python modules installed:\n\trequests, argparse, ssl"
	exit(0)

parser = argparse.ArgumentParser(description="WordPress plugin enumeration")
parser.add_argument('-t','--target', help='WordPress target', required=True)
parser.add_argument('-p','--plugins', help='File containing plugin names', required=True)
parser.add_argument('-o','--outfile', help='Save output in file')
parser.add_argument('-v','--verbose', help='Show verbose message', action='store_const', const=True)
args = parser.parse_args()
target = args.target.encode('utf-8')
plugin_file = args.plugins.encode('utf-8')

if target.endswith("/"):
	target = target[:-1]

if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

print "[*] Started"

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

f = open(plugin_file, "r")
data = f.readlines()

print "\nNote: Append readme.txt or changelog.txt in same or different letter cases to open version file\n"

for i in data:
	try:
		i = (i.replace("\r","")).replace("\n","")
		if args.verbose:
			print "[-] Trying: " + i
		r = requests.get(target+"/wp-content/plugins/"+i+"/", verify=False)
		sc = r.status_code
		if sc != 404 and sc != 500 and sc != 403:
			print i + " : " + str(sc) + " : " + target + "/wp-content/plugins/" + i + "/"
			if args.outfile:
				f = open(args.outfile, "a")
				f.write(i + " : " + str(sc) + " : " + target + "/wp-content/plugins/" + i + "/" + "\n")
				f.close()
	except Exception,e:
		print "Exception occurred"
print "[*] Completed"
