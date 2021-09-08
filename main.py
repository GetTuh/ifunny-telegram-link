from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
from telegram.ext import MessageHandler, Filters

session=HTMLSession()
def getVideoLink(link):
    try:
        link = re.findall(r' - (.*)', link)[0]
        r = session.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find("video").get('data-src')
    except Exception as e:
        return str('e')


from telegram.ext import Updater

updater = Updater(
    token='1869794186:AAG4uMFkSjgSK2qFGnOJo4-UZw-gMxTGNeA', use_context=True
)
dispatcher = updater.dispatcher


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Getting video...')
    videoLink = getVideoLink(update.message.text)
    context.bot.send_photo(update.effective_chat.id, videoLink)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()