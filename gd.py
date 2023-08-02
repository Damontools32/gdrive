import telebot
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import requests

# تنظیمات مربوط به ربات تلگرام
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

# تنظیمات مربوط به گوگل درایو
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
SCOPES = ['https://www.googleapis.com/auth/drive']
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('https://'):
        url = message.text
        upload_to_drive(url)
        bot.reply_to(message, 'لینک با موفقیت در گوگل درایو آپلود شد!')
    else:
        bot.reply_to(message, 'لطفا یک لینک ارسال کنید.')

def upload_to_drive(url):
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES,
        redirect_uri=REDIRECT_URI
    )

    creds = flow.run_local_server(port=0)

    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {
        'name': os.path.basename(url),
        'parents': ['YOUR_PARENT_FOLDER_ID']
    }
