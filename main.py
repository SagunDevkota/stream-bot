import telegram.ext
import bot
from config import TOKEN,PORT,USER1,USER2,TEST_USER


def start(update,context):
    id = update.message.chat.id
    if(id == USER1 or id == USER2 or id == TEST_USER):
        update.message.reply_text("Welcome! to Football Story Bot")
    else:
        update.message.reply_text("""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)

def help(update,context):
    id = update.message.chat.id
    if(id == USER1 or id == USER2 or id == TEST_USER):
        update.message.reply_text("""
        The following commands are available:
        /start -> Welcome Message
        /help -> This Message
        /streams -> list of matches
        """)
    else:
        update.message.reply_text("""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)


def streams(update,context):
    id = update.message.chat.id
    if(id == USER1 or id == USER2 or id == TEST_USER):
        update.message.reply_text("Searching for available matches")
        all_matches_name_list = bot.all_matches_name()
        link_str=''
        if(all_matches_name_list==None):
            update.message.reply_text("We are experiencing problem.Try again later, if problem persists then contact admin")
            return None
        loop_count = 0
        for links in all_matches_name_list:
            link_str+=links+'\n'
            loop_count = loop_count+1
            if((loop_count)%10 == 0):
                update.message.reply_text(link_str)
                link_str = ''
        update.message.reply_text(link_str)
        update.message.reply_text("End Of Detected Matches")
    else:
        update.message.reply_text("""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)

def handle_message(update,context):
    id = update.message.chat.id
    if(id == USER1 or id == USER2 or id == TEST_USER):
        update.message.reply_text("Searching for available streams")
        link_str=''
        sending_message=''
        for chars in update.message.text:
            if(chars=='@'):
                break
            sending_message+=chars
        individual_link = bot.selected_match(bot.all_matches_name(),sending_message)
        if(individual_link==None):
            update.message.reply_text("Match Doesnot Exist make sure you searched the match using /streams command")
            return None
        if(len(individual_link)==0):
            update.message.reply_text("No links found. Links are updated 30min before match. If link is not found till Kick Off then contact admin")
            return None
        for links in individual_link:
            link_str+=links+'\n\n'
        update.message.reply_text(link_str)
        update.message.reply_text("End Of Streaming Links")
    else:
        update.message.reply_text("""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)

updater = telegram.ext.Updater(TOKEN,use_context=True)

disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("help",help))
disp.add_handler(telegram.ext.CommandHandler("streams",streams))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.command,handle_message))
updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TOKEN,
                    webhook_url="https://web-production-104b.up.railway.app/" + TOKEN)
updater.start_polling()
updater.idle()
