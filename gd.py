import telebot
import re

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(func=lambda message: message.text.startswith("https://drive.google.com"))
def handle_google_drive_link(message):

  file_id = re.search(r"(?:/d/|id=)(\w+)", message.text).group(1)

  bot.send_message(message.chat.id, "لطفا نام فایل را ارسال کنید:")

  @bot.message_handler(func=lambda message: True)
  def send_download_link(message):
    filename = message.text
    download_link = f"https://drive.google.com/uc?id={file_id}"
    
    bot.send_message(
      chat_id=message.chat.id,
      text=f"لینک دانلود فایل <b>{filename}</b>:\n{download_link}",
      parse_mode='html'
    )

bot.polling()
