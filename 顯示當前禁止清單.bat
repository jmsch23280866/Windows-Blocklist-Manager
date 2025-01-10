@echo off
set key="HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"

echo 當前阻擋的應用程式清單：
reg query %key% /v * 2>nul | find /i "REG_SZ"
pause
