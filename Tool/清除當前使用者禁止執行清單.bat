@echo off
:: �ˬd�޲z���v���æ۰ʽШD����
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo �ШD�޲z���v��...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:: ��l�{���X�}�l
set key="HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"

for /f "tokens=*" %%A in ('reg query %key% /v * 2^>nul ^| find /i "REG_SZ"') do (
    for /f "tokens=1" %%B in ("%%A") do reg delete %key% /v %%B /f
)
echo �ثe�ϥΪ̩Ҧ��������M��w�Q�R���I
pause
