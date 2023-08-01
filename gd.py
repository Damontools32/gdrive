from telethon.sync import TelegramClient
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# تنظیمات ربات تلگرام
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

# تنظیمات Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# تابع برای آپلود فایل به Google Drive
def upload_to_drive(file_path):
    file_name = file_path.split('/')[-1]
    gfile = drive.CreateFile({'title': file_name})
    gfile.SetContentFile(file_path)
    gfile.Upload()

# تابع برای دریافت لینک مستقیم فایل از ربات تلگرام
def get_direct_link(file_path):
    with TelegramClient('session_name', api_id, api_hash) as client:
        result = client.send_file('me', file_path)
        return result.media.document.url

# مثال استفاده
file_path = 'path/to/your/file.ext'
direct_link = get_direct_link(file_path)
upload_to_drive(file_path)
print('Direct Link:', direct_link)
