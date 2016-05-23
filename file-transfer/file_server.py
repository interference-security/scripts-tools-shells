import socket
import sys

if len(sys.argv)!=3:
    print "\nUsage: file_server.py <port> <filename_to_write>"
    sys.exit(1)
s = socket.socket()
s.bind(("0.0.0.0",int(sys.argv[1])))
s.listen(10)

while True:
    sc, address = s.accept()
    print address
    f = open(sys.argv[2],'wb')
    #while (True):       
    l = sc.recv(102400)
    print "[*] Writing to file"
    while (l):
            f.write(l)
            #print l
            l = sc.recv(102400)
                
    f.close()
    print "[*] File created"
    sc.close()
    break
s.close()
