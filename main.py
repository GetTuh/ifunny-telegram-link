#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from telegram.ext import MessageHandler, Filters
from PIL import Image
from urllib.request import urlopen
import os

session = HTMLSession()


def getVideoLink(link):
    try:
        link = re.findall(r' - (.*)', link)[0]
        type = link.split('/')[3]
        r = session.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        if type == 'picture':
            Image.open(urlopen(soup.find_all('img')[1].get('src'
                       ))).save('temp.jpg')
            with Image.open('temp.jpg') as im:
                (width, height) = im.size
                im_crop = im.crop((0, 0, width, height - 23))
                im_crop.save('temp.jpg')
            return 0
        else:
            return soup.find('video').get('data-src')
    except Exception as e:
        return str('Couldn\'t find image or video')


from telegram.ext import Updater
if not(os.path.isfile('.token')):
    print('.token file doesn\'t exist. Please create the file and include the Telegram token inside.')
    exit()
else:
    with open('.token') as f:
        token = f.readlines()[0].strip()
    updater = Updater(token
                    , use_context=True)
    dispatcher = updater.dispatcher


def echo(update, context):
    videoLink = getVideoLink(update.message.text)
    try:
        context.bot.send_video(update.effective_chat.id, videoLink)
    except:
        context.bot.send_photo(update.effective_chat.id, open('temp.jpg'
                               , 'rb'))
        os.remove('temp.jpg')


echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()
