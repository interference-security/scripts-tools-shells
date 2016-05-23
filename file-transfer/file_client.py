import socket
import sys

if len(sys.argv)!=4:
    print "\nUsage: file_client.py <server_ip_address> <port> <filename_to_transfer>"
    sys.exit(1)
s = socket.socket()
s.connect((sys.argv[1],int(sys.argv[2])))
f=open (sys.argv[3], "rb") 
l = f.read(102400)
while (l):
    s.send(l)
    l = f.read(102400)
s.close()
