#!/usr/bin/python

#Usage:   python port_response_time.py <target_ip> <port_range> <block_size> <connection_timeout> <spawn_processes> <output_filename>
#Example: python port_response_time.py 192.168.1.1 1-65535 10 3 10 port_res_time.out

"""
target_ip : IP Address to scan
port_range : Port range to scan
block_size : Number of blocks of ports to create to be scanned by a process
connection_timeout : Timeout the connection after N seconds
spaw_processes : Number of processes to create for scanning
output_filename : File name  to save output
"""

#Author: Interference Security

import socket
import sys
from datetime import datetime
from multiprocessing import Pool

script_start = datetime.now()
if len(sys.argv)!=7:
	print "Usage: "+sys.argv[0]+" <target_ip> <port_range> <block_size> <connection_timeout> <spawn_processes> <output_filename>"
	exit(0)

target_ip = sys.argv[1]
target_port_range = sys.argv[2].split("-")
block_size = int(sys.argv[3])
con_timeout = int(sys.argv[4])
proc_count = int(sys.argv[5])
out_file = sys.argv[6]

start_port = int(target_port_range[0])
end_port = int(target_port_range[1])

def checker(t_ip, t_port_start, t_port_end):
	res = ""
	for target_port in range(int(t_port_start),int(t_port_end)+1):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(con_timeout)
			start_time = datetime.now()
			sock.connect((t_ip, int(target_port)))
			sock.send("test")
			end_time = datetime.now()
			diff_time = end_time - start_time
			res += target_ip+","+str(target_port)+","+str(diff_time.microseconds)+"\n"
			#print("[*] %s:%s:%s"%(target_ip, target_port, diff_time.microseconds))
		except Exception,e:
			res += target_ip+","+str(target_port)+",Error-"+str(e)+"\n"
			#print("[!] %s:%s:%s"%(target_ip,target_port,"Error-"+str(e)))
	return res

pool = Pool(processes=proc_count)
results = []
for i in range(start_port, end_port, block_size):
	sp = i
	ep = sp + block_size -1
	if ep < end_port:
		results.append(pool.apply_async(checker, args=(target_ip,sp,ep,)))
	else:
		results.append(pool.apply_async(checker, args=(target_ip,sp,end_port,)))
#results.append(pool.apply_async(checker, args=(target_ip,1,10,)))
#results.append(pool.apply_async(checker, args=(target_ip,11,20,)))
#results.append(pool.apply_async(checker, args=(target_ip,21,30,)))
#results.append(pool.apply_async(checker, args=(target_ip,31,40,)))
#results.append(pool.apply_async(checker, args=(target_ip,41,50,)))
f = open(out_file, "w")
for p in results:
	data = p.get()
	f.write(data)
	print data
script_end=datetime.now()
print "Total time: "+str(script_end - script_start)