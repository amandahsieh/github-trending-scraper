import logging
import asyncio
import nest_asyncio
from src.bot.telegram_bot import GithubTrendingBot
from src.bot.key import TELEGRAM_TOKEN

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

async def shutdown():
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    """
    Main function to run the Telegram bot and set up the scheduler.
    """
    # Initialize logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Initialize and run the Telegram Bot
    bot = GithubTrendingBot(token=TELEGRAM_TOKEN)
    logging.info("Starting Telegram Bot...")
    await bot.run()

    try:
        # Keep the program running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Stopping bot...")
        await bot.app.updater.stop()
        await bot.app.stop()
        await bot.app.shutdown()
        logging.info("Bot stopped successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logging.error(f"RuntimeError: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
