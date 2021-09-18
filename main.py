import telegram.ext
import bot
from config import TOKEN,PORT

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
    if(all_matches_name_list==None):
        update.message.reply_text("We are experiencing problem.Try again later, if problem persists then contact admin")
        return None
    for matches_name in all_matches_name_list:
        update.message.reply_text(matches_name)
    update.message.reply_text("End Of Detected Matches")

def handle_message(update,context):
    update.message.reply_text("Searching for available streams")
    individual_link = bot.selected_match(bot.all_matches_name(),update.message.text)
    if(individual_link==None):
        update.message.reply_text("We are experiencing problem.Try again later, if problem persists then contact admin")
        return None
    if(len(individual_link)==0):
        update.message.reply_text("No links found. Links are updated 30min before match. If link is not found till Kick Off then contact admin")
        return None
    for links in individual_link:
        update.message.reply_text(links)
    update.message.reply_text("End Of Streaming Links")


updater = telegram.ext.Updater(TOKEN,use_context=True)

disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("help",help))
disp.add_handler(telegram.ext.CommandHandler("streams",streams))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters._All,handle_message))
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url="https://stream-bot.herokuapp.com/" + TOKEN)
updater.idle()
