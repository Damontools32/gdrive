import telebot
import re 

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(func=lambda message: message.text.startswith("https://drive.google.com"))
def handle_drive_link(message):

  file_id = re.search(r"/d/(.+)", message.text).group(1)

  bot.send_message(message.chat.id, "لطفا نام فایل را وارد کنید:")

  @bot.message_handler(func=lambda message: True)
  def send_download_link(message):
  
    user_filename = message.text
    download_link = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key=YOUR_API_KEY"
    
    bot.send_message(
      chat_id=message.chat.id, 
      text=f"{user_filename}:\n{download_link}"
    )

bot.polling()
