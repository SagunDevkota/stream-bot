import telepot
import re
import config
import botTel
from flask import Flask, render_template, session, url_for, redirect, request
from telepot.namedtuple import *

USERNAME = "hostingsd2"
SECRET = 'abc'
URL = f"https://{USERNAME}.pythonanywhere.com/{SECRET}"

telepot.api.set_proxy('http://proxy.server:3128')
bot = telepot.Bot(config.TOKEN)
bot.setWebhook(URL, max_connections=10)

def processing(msg):
    if 'chat' in msg and msg['chat']['type'] == 'channel':
        return
        
    id = msg['from']['id']
    
    if 'text' in msg:
        msg['text'] = str(msg['text']) # FEELING SAFER ;)
        msg['type'] = 'text'

    elif 'data' in msg:
        msg['type'] = 'callback'
        msg['text'] = f"%callback {msg['data']}"

    else:
        msg['type'] = 'nontext'
        types = ['audio', 'voice', 'document', 'photo',
                 'video', 'contact', 'location']

        for type in types:
            if type in msg:
                msg['text'] = f'%{type}'
                break

    if 'text' in msg:
        for entry in regex:
            if re.match(entry, msg["text"]):
                matches = re.match(entry, msg["text"]).groups()
                parser(msg, list(matches))
                return


app = Flask(__name__)

@app.route(f'/{SECRET}', methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        processing(update['message'])

    elif 'callback_query' in update:
        processing(update['callback_query'])

    return 'OK'

regex = [
    r'^[!/](start)',
    r'^[!/](help)',
    r'^[!/](streams)'
]

def parser(msg, matches):
    usr = msg['from']

    if msg['type'] == "text":
        if matches[0] == 'start':
            bot.sendMessage(usr['id'],"Welcome! to Football Story Bot")
            return

        elif matches[0] == 'help':
            bot.sendMessage(usr['id'], """
        The following commands are available:
        /start -> Welcome Message
        /help -> This Message
        /streams -> list of matches
        """)
            return
        elif matches[0] == 'streams':
            bot.sendMessage(usr['id'],"Searching for available matches")
            all_matches_name_list = botTel.all_matches_name()
            link_str=''
            if(all_matches_name_list==None):
                bot.sendMessage(usr['id'],"""We are experiencing problem.
If problem persists then contact admin""")
                return None
            for links in all_matches_name_list:
                link_str+=links+'\n'
            bot.sendMessage(usr['id'],link_str)
            bot.sendMessage(usr['id'],"End Of Detected Matches")

        else:
            if(len(matches)!=0):
                bot.sendMessage("Searching for available streams")
                link_str=''
                sending_message=matches[0]
                individual_link = bot.selected_mbot.sendMessageatch(botTel.all_matches_name(),sending_message)
                if(individual_link==None):
                    bot.sendMessage("We are experiencing problem.Try again later, if problem persists then contact admin hai tw")
                    return None
                if(len(individual_link)==0):
                    bot.sendMessage("No links found. Links are updated 30min before match. If link is not found till Kick Off then contact admin")
                    return None
                for links in individual_link:
                    link_str+=links+'\n\n'
                bot.sendMessage(link_str)
                bot.sendMessage("End Of Streaming Links")

if __name__ == "__main__":
    app.run()
