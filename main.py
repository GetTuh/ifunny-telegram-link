import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import socket
import os

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_ip())

if __name__ == "__main__":
    if not (os.path.isfile(".token")):
        print(
            ".token file doesn't exist. Please create the file and include the Telegram token inside."
        )
        exit()
    else:
        with open(".token") as f:
            token = f.readlines()[0].strip()
        application = ApplicationBuilder().token(token).build()

        start_handler = CommandHandler("ip", start)
        application.add_handler(start_handler)

        application.run_polling()
