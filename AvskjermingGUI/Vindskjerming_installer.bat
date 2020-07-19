@echo off

:: Make script run as admin
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

echo Downloading Vindskjerming.msi...
set vindskjerming_file="Vindskjerming.msi"
curl -s -L -X GET https://github.com/markhilb/Avskjerming/raw/master/AvskjermingGUI/src/dist/Vindskjerming-0.0.0-win32.msi -o %vindskjerming_file%

set folder="%userprofile%\AppData\Local\Programs\Vindskjerming"
echo Updating Vindskjerming...
msiexec /famus %vindskjerming_file% /l*v netfx.log /qn
IF NOT %errorlevel% == 0 (
    del /f /q "%folder%\*"
    rmdir /s /q "%folder%\lib"
    msiexec /i %vindskjerming_file% /qn
    msiexec /famus %vindskjerming_file%
)

del /f %vindskjerming_file%
del /f netfx.log


set miktex_file="MiKTeX.exe"
IF NOT EXIST "C:\Program Files\MiKTeX" (
    echo Downloading MiKTeX...
    curl -s -L -X GET https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-20.6.29-x64.exe -o %miktex_file%
    echo Installing MiKTeX...
    %miktex_file% ^
        --remote-package-repository=ftp.acc.umu.se ^
        --shared ^
        --unattended
    del /f %miktex_file%
)


set ghostscript_file="GhostScript.exe"
IF NOT EXIST "C:\Program Files (x86)\gs" (
    echo Downloading GhostScript...
    curl -s -L -X GET https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs952/gs952w32.exe -o %ghostscript_file%
    echo Installing GhostScript...
    %ghostscript_file% /S
    del /f %ghostscript_file%
)


echo Done!
pause
exit
