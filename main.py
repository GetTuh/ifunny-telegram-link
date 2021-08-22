from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from telegram.ext import MessageHandler, Filters
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)


def getVideoLink(link):
    try:
        link = re.findall(r' - (.*)', link)[0]
        driver.get(link)
        time.sleep(3)
        elem = driver.find_element_by_tag_name('video')
        return elem.get_attribute('data-src')
    except Exception as inst:
        return str(inst)


from telegram.ext import Updater

updater = Updater(
    token='1869794186:AAG4uMFkSjgSK2qFGnOJo4-UZw-gMxTGNeA', use_context=True
)
dispatcher = updater.dispatcher


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Getting video...')
    videoLink = getVideoLink(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=videoLink)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()
