@echo off
set key="HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun"

for /f "tokens=*" %%A in ('reg query %key% /v * 2^>nul ^| find /i "REG_SZ"') do (
    for /f "tokens=1" %%B in ("%%A") do reg delete %key% /v %%B /f
)
echo ��e�ϥΪ̩Ҧ��T����涵�ؤw�Q�R���I
pause
