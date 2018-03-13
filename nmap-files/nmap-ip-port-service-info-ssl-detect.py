#!/usr/bin/python

#Source: https://github.com/interference-security/scripts-tools-shells/blob/master/nmap-ip-port-service-info.py
#Author: Interference Security

#Usage: nmap-ip-port-service-info.py [-h] -f INPUTFILE [-o OUTFILE]
#Example: nmap-ip-port-service-info.py -f input_nmap.xml -o output_file.csv

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
parser = argparse.ArgumentParser(description="Nmap XML parser and generate CSV ouput")

#Script command line options
parser.add_argument('-i', '--inputfile', help='Input Nmap XML file', required=True)
parser.add_argument('-o','--outfile', help='Save output in CSV file')
#parser.add_argument('-O','--open', help='Show only open ports')

args = parser.parse_args()

targets = []

#Disable requests module HTTPS certificate untrusted warning message
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

def parse_nmap_xml(nmap_xml_file, output_file):
    oufile = ""
    f = None
    if len(output_file)>0:
        f = open (output_file, "w")
    nmap_parse = NmapParser.parse_fromfile(nmap_xml_file)
    for host in nmap_parse.hosts:
        #print host.address+":"
        for service in host.services:
            ssl_status = "No"
            if len(service.scripts_results) > 0:
                for item in service.scripts_results:
                    if item.has_key("id"):
                        if item["id"].lower() == "ssl-enum-ciphers":
                            ssl_status = "Yes"
                #import pdb; pdb.set_trace();
            #if "ssl_status" == "Yes":
            targets.append(host.address+","+str(service.port)+","+str(service.state)+","+service.service+","+service.banner+","+ssl_status)   
            #print service.servicefp
            #print dir(service)
            #print type(service.scripts_results)
            #print service.scripts_results
            #sys.exit(0)
    data = "IP,Port,State,Service Name,Service Info,SSL_TLS"
    print data
    if f != None:
        f.write(data+"\n")
    for target in targets:
        print target
        if f != None:
            f.write(target+"\n")
    return targets

#Main function
output_file = ""
input_file = args.inputfile.encode('utf-8')
if args.outfile:
    output_file = args.outfile
targets = parse_nmap_xml(input_file, output_file)
