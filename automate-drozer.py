import subprocess
import sys

if len(sys.argv)<3:
	print "Usage: " + sys.argv[0] + " <package_name> <drozer_path>"
	print "Usage: " + sys.argv[0] + " <package_name> " + "c:\\drozer\\drozer.bat"
	exit(0)

#Path to your drozer file
drozer_path = sys.argv[2]
#drozer_path = "c:\\drozer\\drozer.bat"
#Store HTML output
html = "<html><head><title>Report: %s</title></head><body><h1>%s</h1>" % (sys.argv[1],sys.argv[1])

def execute_test(test, pname,e=0):
	drozer_cmd = drozer_path + ' console connect -c "run ' + test + ' ' + pname
	if e==1:
		drozer_cmd = drozer_path + ' console connect -c "run ' + test + ' '
	process = subprocess.Popen(drozer_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	input,output,error = process.stdin,process.stdout,process.stderr
	#input.write("hello world !")
	data = output.read().decode('latin1')
	input.close()
	output.close()
	status = process.wait()
	if int(data.find("could not find the package"))!=-1:
		data = "Invalid package"
	else:
		#print "Valid package"
		pass
	return data

def process_data(heading, out):
	html_out = 1
	separator = ("*"*50)
	print "\n%s:\n%s\n%s" % (heading,separator,out)
	out = out.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\\n","<br>").replace("\\r","")
	if html_out:
		global html
		html += "<table border=1 width=100%><tr style='background:#12294d;color:#FFFFFF;'><td>" + heading + "</td></tr><tr><td><pre style='line-height: 0.8em;'>" + out + "</pre></td></tr></table><br><br>"
	
if __name__ == '__main__':
	pname = sys.argv[1]
	separator = ("*"*50)
	#Get package information
	package_info = execute_test('app.package.info -a', pname)
	process_data("Package Information", package_info)
	#Get activity information
	activity_info = execute_test('app.activity.info -i -u -a', pname)
	process_data("Activities Information", activity_info)
	#Get broadcast receiver information
	broadcast_info = execute_test('app.broadcast.info -i -u -a', pname)
	process_data("Broadcast Receivers Information", broadcast_info)
	#Get attack surface details
	attacksurface_info = execute_test('app.package.attacksurface', pname)
	process_data("Attack Surface Information", attacksurface_info)
	#Get package with backup API details
	backupapi_info = execute_test('app.package.backup -f', pname)
	process_data("Package with Backup API Information", backupapi_info)
	#Get Android Manifest of the package
	manifest_info = execute_test('app.package.manifest', pname)
	process_data("Android Manifest File", manifest_info)
	#Get native libraries information
	nativelib_info = execute_test('app.package.native', pname)
	process_data("Native Libraries used", nativelib_info)
	#Get content provider information
	contentprovider_info = execute_test('app.provider.info -u -a', pname)
	process_data("Content Provider Information", contentprovider_info)
	#Get URIs from package
	finduri_info = execute_test('app.provider.finduri', pname)
	process_data("Content Provider URIs", finduri_info)
	#Get services information
	services_info = execute_test('app.service.info -i -u -a', pname)
	process_data("Services Information", services_info)
	#Get native components included in package
	nativecomponents_info = execute_test('scanner.misc.native -a', pname)
	process_data("Native Components in Package", nativecomponents_info)
	#Get world readable files in app installation directory /data/data/<package_name>/
	worldreadable_info = execute_test('scanner.misc.readablefiles /data/data/'+pname+'/', pname, 1)
	process_data("World Readable Files in App Installation Location", worldreadable_info)
	#Get world writeable files in app installation directory /data/data/<package_name>/
	worldwriteable_info = execute_test('scanner.misc.readablefiles /data/data/'+pname+'/', pname, 1)
	process_data("World Writeable Files in App Installation Location", worldwriteable_info)
	#Get content providers that can be queried from current context
	querycp_info = execute_test('scanner.provider.finduris -a', pname)
	process_data("Content Providers Query from Current Context", querycp_info)
	#Perform SQL Injection on content providers
	sqli_info = execute_test('scanner.provider.injection -a', pname)
	process_data("SQL Injection on Content Providers", sqli_info)
	#Find SQL Tables trying SQL Injection
	sqltables_info = execute_test('scanner.provider.sqltables -a', pname)
	process_data("SQL Tables using SQL Injection", sqltables_info)
	#Test for directory traversal vulnerability
	dirtraversal_info = execute_test('scanner.provider.traversal -a', pname)
	process_data("Directory Traversal using Content Provider", dirtraversal_info)
	html += "</body></html>"
	f = open("report.html","w")
	f.write(html)
	f.close()
	print "[*] 'report.html' with testing results saved";
