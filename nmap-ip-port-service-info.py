#!/usr/bin/python

try:
    import sys
    import argparse
    from datetime import datetime
    from libnmap.parser import NmapParser
except:
    print "Error: Missing python packages\n"
    print "Please ensure you have the following python packages installed:\n argparse, python-libnmap\n"
    print "How to install:\npip install <package_name>\neasy_install <package_name>\n"
    sys.exit(0)

#Description of script
parser = argparse.ArgumentParser(description="Nmap IP:PORT")

#Script command line options
parser.add_argument('-f', '--inputfile', help='Input Nmap XML file')

args = parser.parse_args()

targets = []

#Disable requests module HTTPS certificate untrusted warning message
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

def parse_nmap_xml(nmap_xml_file):
    nmap_parse = NmapParser.parse_fromfile(nmap_xml_file)
    for host in nmap_parse.hosts:
        #print host.address+":"
        for service in host.services:
            #targets.append(host.address+","+str(service.port)) #+","+service.service)
            targets.append(host.address+","+str(service.port)+","+service.service+","+service.banner)
            #print service.servicefp
            #print dir(service)
    print "IP,Port,Service Name,Service Info"
    for target in targets:
        print target

    return targets

#Main function
if args.inputfile:
    input_file = args.inputfile.encode('utf-8')
    targets = parse_nmap_xml(input_file)
else:
    print "Missing arguments. Use nmap-ip-port-service-info.py -h"


        
