#openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
import BaseHTTPServer, SimpleHTTPServer, logging
import ssl
import sys
import cgi

class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def do_GET(self):
		#logging.error(self.headers)
		#for item in dir(self):
		#	try:
		#		print "[*] "+item
		#		logging.error(self.item)
		#	except Exception as e:
		#		print str(e)
		#request_path = self.path
		raw_request_line = self.raw_requestline
		#print dir(self)
		#import pdb; pdb.set_trace()
		print "\n----- Request Start ----->"
		print raw_request_line
		print self.headers
		print "<----- Request End ----->"
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		#logging.error(self.headers)
		#form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
		#for item in form.list:
		#	logging.error(item)
		request_path = self.path
		raw_request_line = self.raw_requestline
		print "\n----- Request Start ----->"
		print raw_request_line
		print self.headers
		print "<----- Request End ----->"
		print "<----- Request Body Start ----->"
		print self.rfile.readlines()
		print "<----- Request Body End ----->"
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
	
	do_PUT = do_POST

Handler = GetHandler
listen_ip = sys.argv[1]
listen_port = int(sys.argv[2])
httpd = BaseHTTPServer.HTTPServer((listen_ip, listen_port), Handler)
print "[*] Listening on %s on port %s" % (listen_ip, listen_port)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
httpd.serve_forever()
