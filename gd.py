import telebot
from telebot import types

from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

TELEGRAM_TOKEN = 'XXXXXXXXX:YYYYYYYYY'
SERVICE_ACCOUNT_FILE = 'google-credentials.json'

drive_service = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)) 

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
  print("Got start command")
  bot.reply_to(message, "Hi, send me a file to upload")

@bot.message_handler(content_types=['document'])
def handle_doc(message):
  print("Got document")

  file_id = message.document.file_id
  
  file = bot.get_file(file_id)

  print("Downloading file...")
  downloaded_file = bot.download_file(file.file_path)

  print("Uploading file to Google Drive...")

  drive_file = drive_service.files().create(
    media_body=MediaFileUpload(downloaded_file),
    body={
      'name': file.file_name
    }
  )

  drive_file.execute()

  print("Uploaded successfully!")

  bot.reply_to(message, "File uploaded!")

print("Bot started...")
bot.polling()
