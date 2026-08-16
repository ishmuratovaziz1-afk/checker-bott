Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c ""%TEMP%\checker.bat""", 0, True
