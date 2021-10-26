from config import TOKEN,PORT
import telebot
import bot as bgbot
from flask import Flask,request

app = Flask(__name__)


bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    # bot.reply_to(message, message)
    id = message.from_user.id
    if(id == 753971038 or id == -1001331327568):
        bot.reply_to(message,"Welcome! to Football Story Bot")
    else:
        bot.reply_to("""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)

@bot.message_handler(commands=['help']) # help message handler
def send_help(message):
    id = message.from_user.id
    if(id == 753971038 or id == -1001331327568):
        bot.reply_to(message,"""
        The following commands are available:
        /start -> Welcome Message
        /help -> This Message
        /streams -> list of matches
        """)
    else:
        bot.reply_to(message,"""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)

@bot.message_handler(commands=['streams']) # help message handler
def send_streams(message):
    id = message.from_user.id
    if(id == 753971038 or id == -1001331327568):
        bot.reply_to(message,"Searching for available matches")
        all_matches_name_list = bgbot.all_matches_name()
        link_str=''
        if(all_matches_name_list==None):
            bot.reply_to(message,"We are experiencing problem.Try again later, if problem persists then contact admin")
            return None
        for links in all_matches_name_list:
            link_str+=links+'\n'
        bot.reply_to(message,link_str)
        bot.reply_to(message,"End Of Detected Matches")
    else:
        bot.reply_to(message,"""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)

@bot.message_handler(regexp="^/") # help message handler
def send_links(message):
    id = message.from_user.id
    if(id == 753971038 or id == -1001331327568):
        bot.reply_to(message,"Searching for available streams")
        link_str=''
        sending_message=''
        for chars in message.text:
            if(chars=='@'):
                break
            sending_message+=chars
        individual_link = bgbot.selected_match(bgbot.all_matches_name(),sending_message)
        if(individual_link==None):
            bot.reply_to(message,"We are experiencing problem.Try again later, if problem persists then contact admin hai tw")
            return None
        if(len(individual_link)==0):
            bot.reply_to(message,"No links found. Links are updated 30min before match. If link is not found till Kick Off then contact admin")
            return None
        for links in individual_link:
            link_str+=links+'\n\n'
        bot.reply_to(message,link_str)
        bot.reply_to(message,"End Of Streaming Links")
    else:
        bot.reply_to(message,"""
            We have detected unusual request from your device.
You have been banned from the service until further notice,
        """)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://stream-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)