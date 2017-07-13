# -*- coding: utf-8 -*-
import vk
import telebot
import re
from telebot import types
token = "436381578:AAHOvdsfb9fImJu23F4LocwGp1K0wAnyDzs"
bot = telebot.TeleBot(token)

print "start"

session = vk.Session()
session = vk.AuthSession('5001234', "login", "pass", scope='wall, messages, users')
vk_api = vk.API(session)
api = vk.API(session)

markup = types.ReplyKeyboardMarkup()
markup.row("Unread")
markup1 = types.ReplyKeyboardMarkup()
markup1.row("Next")
 

useusers = []

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    global useusers
    to_remove=[]
    print message.text
    next = False

    b = re.findall('^\d+', message.text)
    c = re.findall('^\d+ (.+)', message.text)
    if len(b)!=0 and len(c)!=0:
        b = int(b[0]) - 1
        c = c[0]
        print b
        print c
        print useusers
        vk_api.messages.send(user_id = useusers[b], message = c)
    if message.text == "Unread":
        useusers = []
        a = vk_api.messages.get(out="0", count = "10")
        a.pop(0)
        a.reverse()
        j = 0
        print a
        while j != len(a):
            i = 0
            firstid = 0
            while i != len(a):
                if a[i]["read_state"] != 1:
                    firstid = a[i]["uid"]
                i += 1
            print "first id " + str(firstid)
            if firstid != 0:
                resp_account = vk_api.users.get(user_ids = firstid)[0]
                bot.send_message(message.chat.id,"user: " + resp_account["first_name"] + " " + resp_account["last_name"])
                useusers.append(firstid)
                
                next = True
            i = 0
            while i != len(a) and firstid != 0:
                print str(a[i]["uid"]) + "==" + str(firstid)+" | " + "readstate ==" + str(a[i]["read_state"])
                if a[i]["uid"] == firstid and a[i]["read_state"] == 0:
                    print len(a)
                    bot.send_message(message.chat.id, a[i]["body"])
                    to_remove.append(a[i])
                i += 1
            k = 0
            while k!= len(to_remove):
                try:
                    a.remove(to_remove[k])
                except:
                    True
                k += 1
            j += 1
        if not next:
            bot.send_message(message.chat.id, "Сообщений нет", reply_markup=markup)
        

if __name__ == '__main__':
     bot.polling(none_stop=True)
