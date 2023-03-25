import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import socket
import argparse

parser = argparse.ArgumentParser(description='Telegram bot token')
parser.add_argument('token', type=str,
                    help='Telegram bot token')
args = parser.parse_args()

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
        application = ApplicationBuilder().token(args.token).build()
        start_handler = CommandHandler("ip", start)
        application.add_handler(start_handler)

        application.run_polling()
