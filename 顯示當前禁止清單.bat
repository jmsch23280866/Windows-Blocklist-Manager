@echo off
set key="HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"

echo ��e���ת����ε{���M��G
reg query %key% /v * 2>nul | find /i "REG_SZ"
pause
