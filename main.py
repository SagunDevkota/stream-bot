import telegram.ext
import bot
from flask import Flask

with open('token.txt','r') as f:
    TOKEN = f.read()

app = Flask(__name__)


def start(update,context):
    update.message.reply_text("Welcome! to Football Story Bot")

def help(update,context):
    update.message.reply_text("""
    The following commands are available:
    /start -> Welcome Message
    /help -> This Message
    /streams -> list of matches
    """)

def streams(update,context):
    update.message.reply_text("Searching for available matches")
    all_matches_name_list = bot.all_matches_name()
    for matches_name in all_matches_name_list:
        update.message.reply_text(matches_name)
    update.message.reply_text("End Of Detected Matches")

def handle_message(update,context):
    update.message.reply_text("Searching for available streams")
    individual_link = bot.selected_match(bot.all_matches_name(),update.message.text)
    for links in individual_link:
        update.message.reply_text(links)
    update.message.reply_text("End Of Streaming Links")

def main():
    updater = telegram.ext.Updater(TOKEN,use_context=True)

    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start",start))
    disp.add_handler(telegram.ext.CommandHandler("help",help))
    disp.add_handler(telegram.ext.CommandHandler("streams",streams))
    disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters._All,handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    app.run(debug=True)