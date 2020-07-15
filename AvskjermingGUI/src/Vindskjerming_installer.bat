@echo off
echo Downloading Vindskjerming.msi...
curl -L -X GET https://github.com/markhilb/Avskjerming/raw/export/AvskjermingGUI/src/dist/Vindskjerming-3.2.2-win32.msi -o Vindskjerming.msi
:: echo Deleting old Vindskjerming...
:: set folder="%userprofile%\AppData\Local\Programs\Vindskjerming"
:: IF EXIST "%folder%" rmdir "%folder%" /s/q
echo Done!
pause
