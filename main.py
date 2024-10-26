import logging
import asyncio
import nest_asyncio
from src.bot.telegram_bot import GithubTrendingBot
from src.scheduler.job_scheduler import schedule_jobs
from src.bot.key import TELEGRAM_TOKEN

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

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

    # Set up the scheduler for fetching GitHub trending data
    logging.info("Setting up the scheduler...")
    schedule_jobs(bot)

    try:
        # Keep the program running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logging.error(f"RuntimeError: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
