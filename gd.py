import telebot
import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TOKEN = 'YOUR_TELEGRAM_TOKEN'
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# تنظیمات گوگل درایو
def get_google_drive_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build(API_NAME, API_VERSION, credentials=creds)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text.startswith('http'):
        # دریافت لینک از پیام
        link = message.text
        
        # دریافت سرویس گوگل درایو
        drive_service = get_google_drive_service()
        
        # ایجاد یک فایل جدید در گوگل درایو
        file_metadata = {
            'name': 'file_name',
            'mimeType': 'application/octet-stream'
        }
        file = drive_service.files().create(body=file_metadata).execute()
        file_id = file.get('id')
        
        # دانلود فایل از لینک و آپلود آن به گوگل درایو
        response = requests.get(link)
        file_data = response.content
        
        # آپلود فایل به گوگل درایو
        upload = drive_service.files().update(
            fileId=file_id,
            media_body=drive_service.media_io.MediaIoBaseUpload(io.BytesIO(file_data), mimetype='application/octet-stream'),
        ).execute()
        
        # ایجاد پیام ارسالی به تلگرام
        chat_id = message.chat.id
        response_message = f"فایل با موفقیت آپلود شد.\nلینک دانلود: https://drive.google.com/file/d/{file_id}"
        
        # ارسال پیام به تلگرام
        bot.send_message(chat_id, response_message)

bot.polling(none_stop=True)
