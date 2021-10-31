import telepot
import re
import config
import botTel
from flask import Flask, render_template, session, url_for, redirect, request
from telepot.namedtuple import *
import time


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
            if re.match(entry, msg["text"]):
                matches = re.match(entry, msg["text"]).groups()
                parser(msg, list(matches))
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
    r'^[!/](streams)'
]

def parser(msg, matches):
    usr = msg['from']

    if msg['type'] == "text":
        if matches[0] == 'start':
            bot.sendMessage(usr['id'],"Welcome! to Football Story Bot")
            return

        if matches[0] == 'help':
            bot.sendMessage(usr['id'], """
        The following commands are available:
        /start -> Welcome Message
        /help -> This Message
        /streams -> list of matches
        """)
            return
        if matches[0] == 'streams':
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

if __name__ == "__main__":
	time.sleep(5)
	bot.setWebhook()
	time.sleep(5)
	bot.setWebhook('https://stream-bot.herokuapp.com/')
	app.run()
