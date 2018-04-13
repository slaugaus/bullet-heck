@echo off
rmdir /S dist\data
pyinstaller -F -w -i data\assets\icon\combined.ico launcher.py
xcopy /E data dist\data\

pause