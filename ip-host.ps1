# The following line read a plain list of IPs from files.  For this demo, I have
# this line commented out and added a line to just define an array of IPs here

$listofIPs = Get-Content IPList.txt

#$listofIPs = "8.8.8.8","8.8.4.4","10.0.0.2","192.168.2.1"

#Lets create a blank array for the resolved names
$ResultList = @()

# Lets resolve each of these addresses
foreach ($ip in $listofIPs)
{
     $result = $null
    
     $currentEAP = $ErrorActionPreference
     $ErrorActionPreference = "silentlycontinue"
    
     #Use the DNS Static .Net class for the reverse lookup
     # details on this method found here: http://msdn.microsoft.com/en-us/library/ms143997.aspx
     $result = [System.Net.Dns]::gethostentry($ip)
    
     $ErrorActionPreference = $currentEAP
    
     If ($Result)
     {
          $hostname = [string]$Result.HostName
          $Resultlist += "$IP,$HOSTNAME"
		  $temp = "$IP,$HOSTNAME"
		  $temp
     }
     Else
     {
          $Resultlist += "$IP,No Hostname found"
		  $temp = "$IP,No Hostname found"
		  $temp
     }
}

# If we wanted to output the results to a text file we could do this, for this
# demo I have this line commented and another line here to echo the results to the screen

$resultlist | Out-File output.csv

$ResultList