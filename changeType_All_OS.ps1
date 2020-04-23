$PathToMonitor = "\\192.168.0.162\czi-share\ОТиС\Казначеев\DL"
$FileSystemWatcher = New-Object System.IO.FileSystemWatcher
$FileSystemWatcher.Path  = $PathToMonitor
$FileSystemWatcher.IncludeSubdirectories = $true
$FileSystemWatcher.Filter = "DallasLock8.0C.msi"
$FileSystemWatcher.EnableRaisingEvents = $true
$Action = {
    $details = $event.SourceEventArgs
    $Name = $details.Name
    $FullPath = $details.FullPath
    $OldFullPath = $details.OldFullPath
    $OldName = $details.OldName
    $ChangeType = $details.ChangeType
    $Timestamp = $event.TimeGenerated
    $text = "{0} was {1} at {2}" -f $FullPath, $ChangeType, $Timestamp
    Write-Host ""
    Write-Host $text -ForegroundColor Green
    Wait-Event -Timeout 40
    Copy-Item -Path $FullPath -Destination \\192.168.0.162\Soft\TestIPS\auto\Auto_Install\PY_Inst -Force
    
    # you can also execute code based on change type here
    switch ($ChangeType)
    {
        'Changed' {        }
        'Created' { 
            Write-Host "Вышла новая сборка"
            Write-Host $FullPath
            Start-Sleep -Seconds 5
            $bn1=$FullPath[-33..-38]
            $bdt1=$FullPath[-21..-30]
            [array]::Reverse($bdt1)
            [array]::Reverse($bn1)
            

            if ($bn1[2] -eq "v"){
                $bn2=$bn1[3..6]
    
            }
            else{
                $bn2=$bn1
    
            }
            $bn=$bn2  -join ''
            $bdt=$bdt1  -join ''
            Set-content \\192.168.0.162\Soft\TestIPS\auto\Auto_Install\PY_Inst\bn.txt $bn
            $a,$b,$c = $bdt.Split(".")
            $d=Switch ($c) 
            {
            "01" {"1"}
            "02" {"2"}
            "03" {"3"}
            "04" {"4"}
            "05" {"5"}
            "06" {"6"}
            "07" {"7"}
            "08" {"8"}
            "09" {"9"}
            "10" {"10"}
            "11" {"11"}
            "12" {"12"}
            "13" {"13"}
            "14" {"14"}
            "15" {"15"}
            "16" {"16"}
            "17" {"17"}
            "18" {"18"}
            "19" {"19"}
            "20" {"20"}
            "21" {"21"}
            "22" {"22"}
            "23" {"23"}
            "24" {"24"}
            "25" {"25"}
            "26" {"26"}
            "27" {"27"}
            "28" {"28"}
            "29" {"29"}
            "30" {"30"}
            "31" {"31"}
            }
            $mo=Switch ($b) 
            {
            "01" {"января"}
            "02" {"февраля"}
            "03" {"марта"}
            "04" {"апреля"}
            "05" {"мая"}
            "06" {"июня"}
            "07" {"июля"}
            "08" {"августа"}
            "09" {"сентября"}
            "10" {"октября"}
            "11" {"ноября"}
            "12" {"декабря"}
            }
            $bdl= "Dallas Lock 8.0-C (сборка" + " " + $bn + " " + "от" + " " + $d + " " + $mo + " " + $a + ")"
            Write-Host $bdl
            Set-content \\192.168.0.162\Soft\TestIPS\auto\Auto_Install\PY_Inst\bdt.txt $bdl
            Write-Host $bn
            $osvch=$Fullpath.Substring(44, 4)
            $osvm = Switch ($osvch)
            {
            "10\D" {"kvn_1909"}
            "2019" {"KVN_2019"}
            "2016" {"KVN_2016"}
            "2012" {"KVN_2012"}
            }
            Set-ExecutionPolicy RemoteSigned  -Scope CurrentUse
            Import-Module VMware.VimAutomation.Core
            Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm: $false
            Connect-VIServer -Server 192.168.13.138 -Protocol https -User kvn -Password 5745Ayc
            Get-Snapshot -VM $osvm -Name install | Foreach-Object {
            Set-VM -VM $_.VM -Snapshot $_ -Confirm:$false}
            Wait-Event -Timeout 5
            Get-VM $osvm | Stop-VM -Confirm:$false
            Wait-Event -Timeout 5
            Get-VM $osvm | Start-VM -Confirm:$false
            Remove-Item -Path $FullPath
        }
            
        'Deleted' { "DELETED"
            # uncomment the below to mimick a time intensive handler
            <#
            Write-Host "Deletion Handler Start" -ForegroundColor Gray
            Start-Sleep -Seconds 4    
            Write-Host "Deletion Handler End" -ForegroundColor Gray
            #>
        }
        'Renamed' { 
            # this executes only when a file was renamed
            $text = "File {0} was renamed to {1}" -f $OldName, $Name
            Write-Host $text -ForegroundColor Yellow
        }
        default { Write-Host $_ -ForegroundColor Red -BackgroundColor White }
    }
}

# add event handlers
$handlers = . {
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Changed -Action $Action -SourceIdentifier FSChange
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Created -Action $Action -SourceIdentifier FSCreate
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Deleted -Action $Action -SourceIdentifier FSDelete
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Renamed -Action $Action -SourceIdentifier FSRename
}

Write-Host "Watching for changes to $PathToMonitor"

try
{
    do
    {
        Wait-Event -Timeout 1
        Write-Host "." -NoNewline
        
    } while ($true)
}
finally
{
    # this gets executed when user presses CTRL+C
    # remove the event handlers
    Unregister-Event -SourceIdentifier FSChange
    Unregister-Event -SourceIdentifier FSCreate
    Unregister-Event -SourceIdentifier FSDelete
    Unregister-Event -SourceIdentifier FSRename
    # remove background jobs
    $handlers | Remove-Job
    # remove filesystemwatcher
    $FileSystemWatcher.EnableRaisingEvents = $false
    $FileSystemWatcher.Dispose()
    "Event Handler disabled."
}