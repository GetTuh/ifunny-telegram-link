from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from telegram.ext import MessageHandler, Filters
from PIL import Image
from urllib.request import urlopen
import os

session=HTMLSession()
def getVideoLink(link):
    try:
        link = re.findall(r' - (.*)', link)[0]
        r = session.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        # true if its an image
        if(soup.find_all("img")[1].get('src')[-1]=="g"):
            Image.open(urlopen(soup.find_all("img")[1].get('src'))).save('temp.jpg')
            with Image.open("temp.jpg") as im:
                width, height = im.size
                im_crop = im.crop((0, 0, width, height-23))
                im_crop.save('temp.jpg')
            return 0
        else:
            return soup.find("video").get('data-src')
    except Exception as e:
        return str('Couldn\'t find image or video')


from telegram.ext import Updater

updater = Updater(
    token='1869794186:AAG4uMFkSjgSK2qFGnOJo4-UZw-gMxTGNeA', use_context=True
)
dispatcher = updater.dispatcher


def echo(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id, text='Getting meme... skrrr')
    videoLink = getVideoLink(update.message.text)
    try:
        context.bot.send_video(update.effective_chat.id, videoLink)
    except:
        context.bot.send_photo(update.effective_chat.id, open('temp.jpg', 'rb'))
        os.remove('temp.jpg')

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()
