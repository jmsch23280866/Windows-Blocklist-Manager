@echo off
powershell write-host "Building BlockListManager..." -ForegroundColor Green
pyinstaller --onefile --noconsole BlockListManager.py
powershell write-host "Build complete! The executable can be found in the dist folder." -ForegroundColor Green
pause 