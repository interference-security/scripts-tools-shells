try:
    import requests
    import sys
except Exception,e:
    print "[!] Error: "+str(e)
    print "[*] Make sure you have the following Python modules installed:\n\BeautifulSoup, requests, sys"
    exit(0)

if(len(sys.argv)!=3):
    print "Usage: " + sys.argv[0] + "<ideone_id> <content>"
    print "Example: " + sys.argv[0] + "abcdef hello"
    exit(0)

#proxies = {"http": "http://127.0.0.1:9092", "https": "http://127.0.0.1:9092",}

#abc123
ideone_id = sys.argv[1]
user_content = sys.argv[2]

#Configuration (First 3 required)
PHPSESSID = ""
JIDEONE = ""
settings = ""
_ga = ""
_gat = ""
__unam = ""

cookies = {"PHPSESSID":PHPSESSID, "JIDEONE":JIDEONE, "settings":settings}
post_data = {"input":"", "source":user_content, "link":ideone_id, "only_save":"false"}
r = requests.post("http://ideone.com/submitedit", data=post_data, cookies=cookies, proxies=proxies, verify=False)
sc = r.text
#print sc
r = requests.post("http://ideone.com/plain/"+ideone_id, data=post_data, cookies=cookies, verify=False)
sc2 = r.text
print sc2
