from telegram.ext import ApplicationBuilder
import logging

class TelegramBot:
    def __init__(self, token, chat_id):
        self.app = ApplicationBuilder().token(token).build()
        self.chat_id = chat_id

    async def send_message(self, text):
        try:
            logging.info(f"Sending message to Telegram: {text}")
            await self.app.bot.send_message(chat_id=self.chat_id, text=text)
            print("Message Sent")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
