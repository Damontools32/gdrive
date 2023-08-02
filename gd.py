import telebot
import re

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(func=lambda msg: msg.text.startswith("https://drive.google.com"))
def get_filename(message):
  bot.reply_to(message, "لطفا نام فایل را بفرستید:")

  @bot.message_handler(func=lambda msg: True) 
  def send_download_link(message):
    filename = message.text
    file_id = re.search(r"/d/(.+)", message.text).group(1)

    download_link = f"https://drive.google.com/uc?id={file_id}" 
    
    bot.send_message(
      message.chat.id,
      f"لینک دانلود <a href='{download_link}'>{filename}</a>",
      parse_mode='HTML'
    )

bot.polling()
