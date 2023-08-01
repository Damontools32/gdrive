import telebot
from telebot import types

from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

bot = telebot.TeleBot("TOKEN")

SERVICE_ACCOUNT_FILE = 'google-credentials.json'

drive_service = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE))

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Hi, send me a file to upload")

@bot.message_handler(content_types=['document'])
def handle_doc(message):
  try:
    file_id = message.document.file_id
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)

    drive_file = drive_service.files().create(
      media_body=MediaFileUpload(downloaded_file),
      body={
        'name': file.file_name
      }
    )

    drive_file.execute()

    bot.reply_to(message, "File uploaded successfully!")

  except Exception as e:
    bot.reply_to(message, f"Oops, something went wrong: {e}")

bot.polling()
