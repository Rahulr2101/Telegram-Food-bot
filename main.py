from telebot import TeleBot
import time
import datetime
import threading
import os
from dotenv import load_dotenv
load_dotenv()

bot = TeleBot(os.getenv('KEY'))

blist = []
glist = []
ycount = 0
ncount = 0

@bot.message_handler(commands=['sendPoll'])
def sendpoll(message):
    d = {'Friday':'Satudary','Satudary':'Sunday'}
    today = datetime.datetime.now()
    day_name = today.strftime("%A")
    
    options = ['YES','NO']
    bot.send_poll(message.chat.id,f"How many of you will have food from staff mess on {d[day_name]} ?",options)
    glist = []
    blist = []
    ycount = 0
    ncount = 0
    


def timer(message):
    while True:
        today = datetime.datetime.now()
        day_name = today.strftime("%A")
        now = datetime.datetime.now()
        time_now = now.strftime("%H:%M:%S")
        print(time_now)
        if time_now == '19:00:00' and (day_name == 'Friday' or day_name == 'Satudary'):
            sendpoll(message)
        time.sleep(1)
        

@bot.message_handler(commands=['start'])
def start(message):
    global botRunning
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    print(chat_member)
    if chat_member.status in ["creator","administrator"]:
        botRunning = True
        bot.reply_to(message,"started")
        thread = threading.Thread(target=timer,args=(message,))
        thread.start()

@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    global ycount
    global ncount
    if pollAnswer.option_ids == [0]:
        ycount += 1
    else:
        ncount += 1
    pass

        
bot.infinity_polling()
