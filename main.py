import telepot
import re
import config
import botTel
from flask import Flask, render_template, session, url_for, redirect, request
from telepot.namedtuple import *

URL = f"https://stream-bot.herokuapp.com/"


bot = telepot.Bot(config.TOKEN)


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
            if re.findall(entry, msg["text"]):
                matches = re.findall(entry, msg["text"]).groups()
                parser(msg, matches)
                return


app = Flask(__name__)

@app.route('/', methods=["POST"])
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
    r'^[!/](streams)',
    r'^[!/].*.vs.*'
]

def parser(msg, matches):
    usr = msg['from']

    if(usr['id']== 753971038 or usr[id] == -1001331327568):
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
                    bot.sendMessage(usr['id'],"Searching for available streams")
                    link_str=''
                    sending_message=matches[0]
                    individual_link = bot.selected_mbot.sendMessageatch(botTel.all_matches_name(),sending_message)
                    if(individual_link==None):
                        bot.sendMessage(usr['id'],"We are experiencing problem.Try again later, if problem persists then contact admin hai tw")
                        return None
                    if(len(individual_link)==0):
                        bot.sendMessage(usr['id'],"No links found. Links are updated 30min before match. If link is not found till Kick Off then contact admin")
                        return None
                    for links in individual_link:
                        link_str+=links+'\n\n'
                    bot.sendMessage(usr['id'],link_str)
                    bot.sendMessage(usr['id'],"End Of Streaming Links")
        else:
            bot.sendMessage(usr['id'],"You are banned.")

if __name__ == "__main__":
    bot.setWebhook(URL, max_connections=10)
    app.run()
