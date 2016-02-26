#!/usr/bin/python

#Usage:   python censys_ip_port_info.py <ip_file>
#Example: python censys_ip_port_info.py ip_list.lst

#Data source: https://www.censys.io/

#Author: Inteference Security

import sys
import json
import requests

f = open(sys.argv[1],"r")
all_ips = f.readlines()
for ip_addr in all_ips:
	API_URL = "https://www.censys.io/api/v1"
	UID = "595ed876-6ec3-46dc-bd1f-63ea1c54b259"
	SECRET = "LNIMr24I5lgrZZ3zw7JytDEA1LHYU8yQ"
	ip_addr = (ip_addr.replace("\r","")).replace("\n","")
	post_data = '{"query":"'+ip_addr+'", "fields":["ip", "protocols"]}'

	res = requests.post(API_URL + "/search/ipv4", auth=(UID, SECRET), data=post_data)
	if res.status_code != 200:
		print ip_addr + ",Error,Error"
	else:
#		print res.text
		if len(res.json()["results"])>0:
			temp = (res.json()["results"])[0]
			res_ip = temp["ip"]
			res_protocols = temp["protocols"]
			for port_protocol in res_protocols:
				pp = port_protocol.split("/")
				print res_ip + "," + pp[0] + "," + pp[1]
