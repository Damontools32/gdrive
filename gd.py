from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from telegram import Filters


gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def start(update, context):
    update.message.reply_text('Please send me the link')

def link_handler(update, context):
    url = update.message.text
    file = drive.CreateFile({'title': 'My file'})
    file.SetContentFromUrl(url)
    file.Upload()
    update.message.reply_text('File uploaded to Google Drive')

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, link_handler))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
