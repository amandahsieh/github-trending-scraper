import logging
import asyncio
from src.bot.telegram_bot import TelegramBot
from src.bot.key import TELEGRAM_TOKEN, CHAT_ID
from src.scheduler.scheduler import setup_scheduler

async def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot = TelegramBot(token=TELEGRAM_TOKEN, chat_id=CHAT_ID)
    setup_scheduler(bot)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")

if __name__ == "__main__":
    asyncio.run(main())
