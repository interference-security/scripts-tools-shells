#!/usr/bin/python

#Usage:   python shodan_ip_port_info.py <input_ip_list_file> <output_file>
#Example: python shodan_ip_port_info.py ip_list.lst output.out

#Note: As on 27-02-2016 this command "shodan host <ip_address>" does not use Shodan API and does not consume your credits

#Author: Interference Security

import sys
from subprocess import check_output

o = open(sys.argv[1], "r")
data = o.readlines()
for ipaddr in data:
	ipaddr = (ipaddr.replace("\n","")).replace("\r","")
	try:
		out = check_output(["shodan", "host", ipaddr])
		f = open(sys.argv[2], "a")
		f.write(out)
		f.write("\n")
		print out
		f.close()
	except:
		pass
