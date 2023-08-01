import telebot
from pydrive.drive import GoogleDrive

TELEGRAM_TOKEN = 'xxxxxxxxx:yyyyyyyyy'

bot = telebot.TeleBot(TELEGRAM_TOKEN) 

@bot.message_handler(content_types=['document'])
def handle_document(message):

  file_id = message.document.file_id
  
  file = bot.get_file(file_id)
  
  downloaded_file = bot.download_file(file.file_path)

  gauth = GoogleAuth()
  
  # Authorization 
  gauth.CommandLineAuth() 

  drive = GoogleDrive(gauth)

  uploaded_file = drive.CreateFile({'title': file.file_name})
  uploaded_file.SetContentString(downloaded_file)
  uploaded_file.Upload()

  bot.reply_to(message, "File uploaded successfully!")

bot.polling()
