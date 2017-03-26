$usbdrives = Get-WmiObject Win32_Volume -Filter "DriveType='2'"|select -expand driveletter
$usbdrives = $usbdrives.Trim(":")
#THIS WILL FORMAT THE DRIVE
#Format-Volume -DriveLetter $usbdrives -NewFileSystemLabel MyDrive -FileSystem NTFS -Confirm:$false
#notepad $usbdrives
Unregister-Event -SourceIdentifier volumeChange -ErrorAction SilentlyContinue
Register-WmiEvent -Class win32_VolumeChangeEvent -SourceIdentifier volumeChange -ErrorAction SilentlyContinue
#write-host (get-date -format s) " Beginning script..."
do
{
    $newEvent = Wait-Event -SourceIdentifier volumeChange
    $eventType = $newEvent.SourceEventArgs.NewEvent.EventType
    $eventTypeName = switch($eventType)
    {
        1 {"Configuration changed"}
        2 {"Device arrival"}
        3 {"Device removal"}
        4 {"docking"}
        }
    #write-host (get-date -format s) " Event detected = " $eventTypeName
    if ($eventType -eq 2)
    {
        $driveLetter = $newEvent.SourceEventArgs.NewEvent.DriveName
        $driveLabel = ([wmi]"Win32_LogicalDisk='$driveLetter'").VolumeName
        #write-host (get-date -format s) " Drive name = " $driveLetter
        #write-host (get-date -format s) " Drive label = " $driveLabel
        $driveLetter = $driveLetter.Trim(":")
        #write-host $driveLetter
    
        #THIS WILL FORMAT THE DRIVE
        #Format-Volume -DriveLetter $driveLetter -NewFileSystemLabel MyDrive -FileSystem NTFS -Confirm:$false
        #calc

        # Execute process if drive matches specified condition(s)
        #if ($driveLetter -eq 'Z:' -and $driveLabel -eq 'Mirror')
        #{
        #    write-host (get-date -format s) " Starting task in 3 seconds..."
        #    start-sleep -seconds 3
        #    start-process "Z:\sync.bat"
        #}
    }
    Remove-Event -SourceIdentifier volumeChange -ErrorAction SilentlyContinue
} while (1-eq1) #Loop until next event
Unregister-Event -SourceIdentifier volumeChange -ErrorAction SilentlyContinue