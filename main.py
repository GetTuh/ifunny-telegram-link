#!/usr/bin/python
# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import os
import socket

session = HTMLSession()


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    s.close()
    return ip

if not (os.path.isfile('.token')):
    print('.token file doesn\'t exist. Please create the file and include the Telegram token inside.')
    exit()
else:
    with open('.token') as f:
        token = f.readlines()[0].strip()
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

def echo(update, context):
    if (update.message.text == 'ip'):
        context.bot.send_message(
            text=getIP(), chat_id=update.effective_chat.id)


echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()
